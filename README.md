# Scientific Relation Extraction with PURE + SciBERT

이 프로젝트는 SciERC processed data(`train.json`, `dev.json`, `test.json`)와 Princeton PURE + SciBERT를 사용해서 scientific entity/relation extraction을 실행하고, 결과를 relation table과 knowledge graph로 바꾸는 템플릿입니다.

## 0. 폴더 배치

최종 구조는 아래처럼 맞추면 됩니다.

```text
scierc_pure_project/
├── external/
│   └── PURE/                       # git clone한 PURE 원본 repo
├── data/
│   └── scierc/
│       └── processed_data/
│           └── json/
│               ├── train.json
│               ├── dev.json
│               └── test.json
├── models/
├── outputs/
├── scripts/
└── src/
```

네가 이미 `processed_data` 폴더를 넣었다면, 아래 위치로 맞추세요.

```text
data/scierc/processed_data/json/train.json
data/scierc/processed_data/json/dev.json
data/scierc/processed_data/json/test.json
```

## 1. 설치

먼저 이 프로젝트 requirements를 설치합니다.

```bash
pip install -r requirements.txt
```

그 다음 PURE 원본 repo를 넣습니다.

```bash
mkdir external
git clone https://github.com/princeton-nlp/PURE.git external/PURE
pip install -r external/PURE/requirements.txt
```

## 2. 폴더 생성 및 데이터 확인

```bash
python scripts/00_setup_project.py
python scripts/01_check_scierc.py
```

정상이라면 train/dev/test 문서 수, entity 수, relation 수가 출력됩니다.

## 3. PURE entity model 훈련 또는 평가

처음에는 pre-trained model을 쓰는 게 빠릅니다. 네가 직접 훈련하고 싶으면 아래 명령을 사용합니다.

```bash
python scripts/03_train_entity.py
```

훈련 결과는 기본적으로 아래에 저장됩니다.

```text
models/fine_tuned/entity/
```

pretrained model을 이미 받아둔 경우, entity prediction만 실행하려면:

```bash
python scripts/05_run_entity.py --output_dir models/scierc_ent_model/ent-scib-ctx0 --eval_test
```

## 4. PURE relation model 훈련 또는 평가

entity model이 먼저 필요합니다. relation model은 entity model 출력 폴더를 입력으로 사용합니다.

```bash
python scripts/04_train_relation.py --entity_output_dir models/fine_tuned/entity
```

pretrained relation model을 이미 받아둔 경우:

```bash
python scripts/06_run_relation.py ^
  --entity_output_dir models/scierc_ent_model/ent-scib-ctx0 ^
  --output_dir models/scierc_rel_model/rel-scib-ctx0 ^
  --eval_test
```

Windows PowerShell에서는 `^` 대신 백틱(`)을 써도 됩니다.

## 5. PURE 평가 결과 출력

```bash
python scripts/07_eval_predictions.py --prediction_file models/scierc_rel_model/rel-scib-ctx0/predictions.json
```

## 6. relation table 만들기

PURE prediction 파일이나 SciERC gold file에서 relation table을 만들 수 있습니다.

### gold test data로 바로 테스트

```bash
python scripts/08_extract_triples.py ^
  --input_file data/scierc/processed_data/json/test.json ^
  --mode gold ^
  --output_csv outputs/tables/relation_table_gold_test.csv
```

### PURE prediction으로 추출

```bash
python scripts/08_extract_triples.py ^
  --input_file models/scierc_rel_model/rel-scib-ctx0/predictions.json ^
  --mode predicted ^
  --output_csv outputs/tables/relation_table_pred_test.csv
```

## 7. 중복 triple 병합

여러 paper에서 같은 `(entity, relation, entity)`가 나오면 하나로 합치고 `support_count`를 올립니다.

```bash
python scripts/09_merge_triples.py ^
  --input_csv outputs/tables/relation_table_pred_test.csv ^
  --output_csv outputs/tables/merged_triples.csv
```

## 8. graph 생성

```bash
python scripts/10_build_graph.py ^
  --input_csv outputs/tables/merged_triples.csv ^
  --nodes_csv data/processed/graph/graph_nodes.csv ^
  --edges_csv data/processed/graph/graph_edges.csv ^
  --graph_json data/processed/graph/graph_data.json

python scripts/11_visualize_graph.py ^
  --graph_json data/processed/graph/graph_data.json ^
  --output_html outputs/figures/relation_graph.html
```

그래프 표현 방식:

- node color = entity type
- edge color = relation type
- edge thickness = support_count
- hover = source paper list

## 9. 한 번에 gold data graph 만들기

PURE 모델을 돌리기 전에 구조 확인용으로 gold annotation 기반 graph를 바로 만들 수 있습니다.

```bash
python scripts/12_run_gold_graph_demo.py
```

## 10. abstract CSV 입력 형식

`data/demo_inputs/abstracts_sample.csv` 형식:

```csv
paper_id,title,abstract,source
paper_001,BERT Relation Extraction,"We propose a BERT-based model for relation extraction.",manual
```

abstract를 PURE 입력 형식으로 바꾸려면:

```bash
python scripts/02_prepare_demo_input.py ^
  --input_csv data/demo_inputs/abstracts_sample.csv ^
  --output_dir data/processed/pure_input/demo_data
```

주의: PURE 원본은 기본적으로 `train/dev/test.json` 구조를 기대합니다. 이 스크립트는 `demo_data/test.json`을 만들어서 PURE의 `--data_dir demo_data --eval_test` 흐름에 맞춥니다. 다만 gold annotation이 없는 custom abstract에서는 PURE 원본 평가 코드가 gold count 0 문제를 낼 수 있어, 첫 실행은 SciERC test set으로 먼저 검증하는 것을 추천합니다.
