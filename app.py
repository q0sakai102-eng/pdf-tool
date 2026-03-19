import streamlit as st
import opendataloader_pdf
import tempfile
import os

st.set_page_config(page_title="PDF変換ツール", layout="centered")
st.title("PDF変換ツール")

uploaded_files = st.file_uploader(
    "PDFをアップロード（複数OK）",
    type="pdf",
    accept_multiple_files=True,
)

format_option = st.selectbox(
    "出力フォーマット",
    ["markdown", "json", "html", "markdown,json"],
)

if st.button("変換する") and uploaded_files:
    with st.spinner("変換中...しばらくお待ちください"):
        with tempfile.TemporaryDirectory() as tmpdir:
            input_paths = []
            for f in uploaded_files:
                path = os.path.join(tmpdir, f.name)
                with open(path, "wb") as out:
                    out.write(f.read())
                input_paths.append(path)

            output_dir = os.path.join(tmpdir, "output")
            os.makedirs(output_dir)

            opendataloader_pdf.convert(
                input_path=input_paths,
                output_dir=output_dir,
                format=format_option,
            )

            st.success(f"変換完了！ {len(uploaded_files)}件のPDFを処理しました")

            for filename in sorted(os.listdir(output_dir)):
                filepath = os.path.join(output_dir, filename)
                with open(filepath, "r", encoding="utf-8") as result:
                    content = result.read()
                st.download_button(
                    label=f"ダウンロード: {filename}",
                    data=content,
                    file_name=filename,
                )
                with st.expander(f"プレビュー: {filename}"):
                    st.code(content)
