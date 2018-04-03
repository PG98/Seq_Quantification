## Pipelline

#### Week1 - FPKM

**Required packages: fastqc, sra-tools, STAR, samtools, cufflinks**

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

  * Indices 

    ```bash
    srun STAR --runThreadN 4 --runMode genomeGenerate --genomeDir indices/STAR --genomeFastaFiles hg19_index/hg19.fa --sjdbGTFfile hg19_index/hg19.gtf &
    ```

  * Align

    http://www.bio-info-trainee.com/727.html

    http://blog.sina.com.cn/s/blog_17a1407140102xp4j.html

    ```bash
    STAR --runThreadN 20 --genomeDir /home/sjchen/indices/STAR --readFilesIn /data/hca/Patel_fastq/new3_unzip/SRR1295114_1.fastq /data/hca/Patel_fastq/new3_unzip/SRR1295114_2.fastq --outFileNamePrefix /home/sjchen/results/STAR/SRR1295114/ --outSAMtype BAM SortedByCoordinate
    ```

* Cufflinks

  * cufflink

    samtobam

    http://cole-trapnell-lab.github.io/cufflinks/manual/

    %先用 samtools 将 align 生成的 sam 文件正确排序（以后可以在align时加参数）

    ```bash
    samtools #TODO: the sam file has to be sorted for downstream(cufflink)
    ```

    ```
    cufflinks -p 8 -G /home/sjchen/hg19_index/ref_smartseq/hg19.gtf  -o /home/sjchen/results/cuff /home/sjchen/results/STAR/Aligned.out.sam >/home/sjchen/results/cufflinks.log
    ```

    ​

http://blog.sciencenet.cn/blog-1113671-1038659.html