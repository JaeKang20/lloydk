import pandas as pd
from tqdm import tqdm

# 원본 JSON 파일 경로
original_file_path = 'sample.json'

# 새로 저장할 ndjson 파일 경로
new_file_path = 'formattedSample.json'

# Pandas DataFrame 초기화
df = pd.DataFrame()

# 파일을 조금씩 읽어들여 DataFrame에 추가
chunk_size = 1000  # 적절한 크기로 조절
total_lines = sum(1 for line in open(original_file_path, 'r', encoding='utf-8'))

# tqdm으로 감싸주면서 파일 읽기 루프에 진행바 추가
with tqdm(total=total_lines, desc="Reading JSON", unit="lines") as pbar:
    for chunk in pd.read_json(original_file_path, lines=True, chunksize=chunk_size):
        df = pd.concat([df, chunk], ignore_index=True)
        pbar.update(chunk.shape[0])

# DataFrame을 ndjson 파일로 저장 (newline delimited JSON), elastic은 ndjson 지원
df.to_json(new_file_path, orient='records', lines=True, force_ascii=False, date_format='iso')

print(f'포맷팅된 ndjson 파일이 {new_file_path}에 저장되었습니다.')
print(f'객체 개수: {len(df)}')
