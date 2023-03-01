FROM ubuntu:22.04

RUN apt update && apt install -y \
    tesseract-ocr \
    python3 \
    && rm -rf /var/lib/apt/lists/*

ADD https://github.com/tesseract-ocr/tessdata_best/blob/e2aad9b983032bb1beff9133104a67cdbb87ca4d/eng.traineddata?raw=true /usr/share/tesseract-ocr/4.00/tessdata/
ADD https://github.com/tesseract-ocr/tessdata_best/blob/e2aad9b983032bb1beff9133104a67cdbb87ca4d/jpn.traineddata?raw=true /usr/share/tesseract-ocr/4.00/tessdata/
ADD https://github.com/tesseract-ocr/tessdata_best/blob/e2aad9b983032bb1beff9133104a67cdbb87ca4d/jpn_vert.traineddata?raw=true /usr/share/tesseract-ocr/4.00/tessdata/
