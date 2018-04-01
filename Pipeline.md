### Pipeline

* fastq-dump

  * ```bash
    fastq-dump -O new3_unzip --split-files SRR1294493 SRR1294495 &
    ```

* fastqc

  * ```bash
    fastqc -o ./FastQC/fastqc_result/ -t 1 ./FastQC/fastqc_raw_data/*.fastq
    ```

* Trim

  * ```bash
    AdapterRemoval --file1 reads_1.fq --file2 reads_2.fq --basename output_paired --trimns --trimqualities --collapse
    ```

* STAR

  * index

    * ```bash
      nohup srun STAR --runThreadN 4 --runMode genomeGenerate --genomeDir indices/STAR --genomeFastaFiles hg19_index/hg19.fa --sjdbGTFfile hg19_index/hg19.gtf &
      ```

  * align

    ```bash
    STAR --runThreadN 4 --genomeDir indices/STAR --readFilesIn  CFY/new3_unzip/SRR*.fastq --outFileNamePrefix results/STAR/

    ```

