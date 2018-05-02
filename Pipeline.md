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




# TPM

## Salmon

[官网](http://combine-lab.github.io/salmon/)

[Documentation](http://salmon.readthedocs.io/en/latest/salmon.html#using-salmon)

### Build index

```bash
salmon index -t /home/sjchen/hg19_index/kallisto/Homo_sapiens.GRCh38.cdna.all.fa.gz -i Homo_Sapiens_Salmon_index > indexGen.log 2>&1
```

### Quantify

```bash
#salmon quant -i transcripts_index -l <LIBTYPE> -r reads.fq -o transcripts_quant
salmon quant -i /home/sjchen/hg19_index/salmon/Homo_Sapiens_Salmon_index -l A -r reads.fq -o transcripts_quant
```





## Read counts

## HT-seq

```bash
htseq-count -f bam /data/hca/tumor/SRR522108./Aligned.sortedByCoord.out.bam /home/sjchen/hg19_index/ref_smartseq/hg19.gtf > /data/hca/tumor/SRR522108./SRR522108.count
```



## Kallisto

(后续处理的R包： sleuth)

[官网](https://pachterlab.github.io/kallisto/)

[参考资料1](https://wenku.baidu.com/view/21c4991d76232f60ddccda38376baf1ffc4fe3a8.html)

```bash
# indexing
kallisto index -i transcripts.idx Homo_sapiens.GRCh38.cdna.all.fa.gz
```



## RSEM

[官网](https://github.com/deweylab/RSEM)

- 非链特异性 --strandedness none





# RPKM

## NURD







## Hisat + Stringtie

* Reference
  * hisat 使用：
    * http://blog.sciencenet.cn/home.php?mod=space&uid=1469385&do=blog&id=1022768
    * http://www.bio-info-trainee.com/731.html
    * http://www.chenlianfu.com/?p=2284


* 下载官网索引 (optional)

```bash
axel -n 10 ftp://ftp.ccb.jhu.edu/pub/infphilo/hisat2/data/hg38.tar.gz
```

* Indexing

```bash
# The two python scripts should be availatble when hisat is installed in the current anaconda environment.
# Before indexing, convert .gtf file to what hisat2-build could handle.
hisat2_extract_exons.py ~/hg19_index/ref_smartseq/hg19.gtf > genome.exon
hisat2_extract_splice_sites.py ~/hg19_index/ref_smartseq/hg19.gtf > genome.ss &
```

​	建立索引：

```bash
hisat2-build -p 10 genome.fa --snp genome.snp --ss genome.ss --exon genome.exon genome_snp_tran
```

* Alignment

```bash
hisat -x  my_hisat_index -U ../reads/reads_1.fq  -S reads1.sam
```



* quant