"""
Phase 1 테스트: Google Sheets 데이터 로드 확인
"""

from utils.data_loader import load_all_data


def main():
    # 4개 시트 전체 로드
    data = load_all_data()

    print("\n" + "=" * 50)
    print("데이터 로드 결과 요약")
    print("=" * 50)

    for key, df in data.items():
        print(f"\n--- {key} ---")
        print(f"  크기: {df.shape[0]}행 x {df.shape[1]}열")
        print(f"  컬럼: {list(df.columns)}")
        print(df.head(3).to_string(index=False))


if __name__ == "__main__":
    main()
