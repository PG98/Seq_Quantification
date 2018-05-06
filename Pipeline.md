## Pipelline

####  FPKM

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


## Tophat + Cufflinks

* Create a new anaconda environment under python v2.7


```bash
conda create --name py27 python=2.7
```

* Indexing with bowtie2

最后的 genome 使得输出文件以 genome 开头，形如 “genome.1.bt2”

```bash
bowtie2-build --threads 15 /home/sjchen/hg19_index/ref_smartseq/hg19.fa /home/sjchen/hg19_index/tophat/genome
```

* Alignment (which is unbearably slow)

其中 genome 是上一步生成 index 中对索引文件的命名

```bash
tophat2 -p 8 -G <xxx/hg19.gtf> -o <outDIR> <indexDIR>/genome <xxx/xxx.fastq> >%s/mapping.log
```

* Cufflinks (TBD)




# TPM

## Salmon

[官网](http://combine-lab.github.io/salmon/)

[Documentation](http://salmon.readthedocs.io/en/latest/salmon.html#using-salmon)

### Build index

```bash
salmon index -t /home/sjchen/hg19_index/kallisto/Homo_sapiens.GRCh38.cdna.all.fa.gz -i Homo_Sapiens_Salmon_index > indexGen.log 2>&1
```

### Quantification

```bash
#salmon quant -i transcripts_index -l <LIBTYPE> -r reads.fq -o transcripts_quant
salmon quant -i /home/sjchen/hg19_index/salmon/Homo_Sapiens_Salmon_index -l A -r reads.fq -o transcripts_quant
```





## Read counts

## HT-seq

```bash
#  (Using STAR alignment results)
htseq-count -f bam /data/hca/tumor/SRR522108./Aligned.sortedByCoord.out.bam /home/sjchen/hg19_index/ref_smartseq/hg19.gtf > /data/hca/tumor/SRR522108./SRR522108.count
```



## Kallisto

(后续处理的R Package： sleuth)

[官网](https://pachterlab.github.io/kallisto/)

[参考资料1](https://wenku.baidu.com/view/21c4991d76232f60ddccda38376baf1ffc4fe3a8.html)

* Index

```bash
# indexing
kallisto index -i transcripts.idx Homo_sapiens.GRCh38.cdna.all.fa.gz
```

* Quantification

```bash
kallisto quant -t 8 -i /home/sjchen/hg19_index/kallisto/transcripts.idx -o <outputPath> -b 100 --single -l 180 -s 20 xxx.fastq
```





## RSEM

[官网](https://github.com/deweylab/RSEM)

- 非链特异性 --strandedness non


* 建立索引

  ### rsem-prepare-reference 

```bash
rsem-prepare-reference --gtf /home/sjchen/hg19_index/rsem/Homo_sapiens.GRCh38.83.gtf --star /home/sjchen/hg19_index/rsem/Homo_sapiens.GRCh38.dna.primary_assembly.fa /home/sjchen/hg19_index/rsem/human_ref
```

#### rsem-calculate-expression

If we feed STAR alignments to rsem, then the previous alignment(BAM) should be  with respect to the transcriptome rather than to the genome(default). (TBD, May 3rd.)

```bash
rsem-calculate-expression -p 15 --bam --estimate-rspd --append-names --output-genome-bam  .../Aligned.toTranscriptome.out.bam .../<index> .../<outputDIR> > calctest.log 2>&1
```

注：以上使用的Aligned to transcriptome 对应的STAR命令：

```bash
STAR --runThreadN 8 --genomeDir %s --readFilesIn %s --outFileNamePrefix %s --outSAMtype BAM SortedByCoordinate  --quantMode TranscriptomeSAM
```





# RPKM

## NURD







## Hisat + Stringtie

* Reference
  * hisat 使用：
    * http://blog.sciencenet.cn/home.php?mod=space&uid=1469385&do=blog&id=1022768
    * http://www.bio-info-trainee.com/731.html
    * http://www.chenlianfu.com/?p=2284
  * Stringtie
    * http://blog.163.com/bioinfo_wen/blog/static/234301034201751393430440/
    * ​


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
hisat --dta -x  my_hisat_index -U ../reads/reads_1.fq  -S reads1.sam
# 官网：be sure to run HISAT2 with the --dta option for alignment, or your results will suffer
```

* Sam to bam:

```bash
samtools sort -@ 8 -o ...output/xxx.bam input/xxx.sam
```

* quant

```bash
stringtie <xxx.bam> -G hg19.gtf(genomePath) -p 20 -b <outputDIR> -e -o <outputDIR/gtfname.gtf>
```

* merge

**gtfList 是包含待merge样本的gtf，'\n'分割的文本文件。**

```bash
stringtie --merge -p 20 -G xxx/hg19.gtf -o <outpath/xxx.gtf> <gtfList>
```

* 利用上一步merge结果，重新quant

```bash
stringtie <bamDIR> -G xxx/merged.gtf -p 20 -b <outputDIR> -e -o <outputDIR/outfilename.gtf>
```

