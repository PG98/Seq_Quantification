## Pipelline

#### Week1 - FPKM

**Required packages: fastqc, sra-tools, STAR, samtools, cufflinks**

* fastq-dump

  * ```bash
    fastq-dump -O new3_unzip --split-files SRR1294493 &
    ```

* fastqc

  * ```bash
    fastqc -o ./FastQC/fastqc_result/ -t 1 ./FastQC/fastqc_raw_data/*.fastq
    ```

* Trim (not in bulk)

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
    STAR --runThreadN 20 --genomeDir /home/sjchen/indices/STAR/
    --readFilesIn /data/hca/Patel_fastq/new3_unzip/SRR1295114_1.fastq /data/hca/Patel_fastq/new3_unzip/SRR1295114_2.fastq --outFileNamePrefix /home/sjchen/results/STAR/SRR1295114/ --outSAMtype BAM SortedByCoordinate  --outSAMstrandField intronMotif
    ```

    * 加上 strandField参数后文件里会有特定的 attribute, which is vital for cufflinks

* Cufflinks (version 2.2.1)

  * cufflinks

    samtobam (optional, v2.2.1 supports .bam format)

    http://cole-trapnell-lab.github.io/cufflinks/manual/

    %先用 samtools 将 align 生成的 sam 文件正确排序（以后可以在align时加参数）

    ```bash
    samtools #TODO: the sam file has to be sorted for downstream(cufflink)
    ```

    ```
    cufflinks -p 8 -G /home/sjchen/hg19_index/ref_smartseq/hg19.gtf  -o /home/sjchen/results/cuff /home/sjchen/results/STAR/Aligned.out.sam >/home/sjchen/results/cufflinks.log
    ```

    --library-type fr-secondstrand

http://blog.sciencenet.cn/blog-1113671-1038659.html

* Cuffmerge


* Cuffquant

  ```shell
  cuffquant -p 8 --no-update-check -o quant /home/sjchen/results/cuffmerge/merged.gtf /home/sjchen/results/STARtoCuff/SRR1294494/Aligned.sortedByCoord.out.bam
  ```

* Cuffnorm

  使用cuffnorm进行基因和转录本表达水平的标准化处理.

  **参数中最后的cxb不是 comma-separated 而是 space; bam/sam 也接受，但所有文件类别须一致**

  ```shell
  cuffnorm -o cuffnorm_out -p 8 -L SRR1295210,SRR1295211... /home/songshaoming/data/HCA/genome.gtf /home/songshaoming/data/HCA/SRR1295210_quant/abundances.cxb,/home/songshaoming/data/HCA/SRR1295211_quant/abundances.cxb,...

  ```

* Plot using R or py 




## Read counts

## HT-seq

```bash
htseq-count -f bam /data/hca/tumor/SRR522108./Aligned.sortedByCoord.out.bam /home/sjchen/hg19_index/ref_smartseq/hg19.gtf > /data/hca/tumor/SRR522108./SRR522108.count
```



## Kallisto

(后续处理的R包： sleuth)

```bash
# indexing
kallisto index -i transcripts.idx Homo_sapiens.GRCh38.cdna.all.fa.gz
```

