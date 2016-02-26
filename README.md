# Pantip-Libr

Pantip librarian!

## What is Pantip?

[Pantip](http://www.pantip.com) is the biggest online Q&A community 
in Thailand founded in 1996. Pantip stores a very large 
user-generated questions and answers in numberous topics, 
e.g., lifestyle, health, tradings, technologies, sciences, 
sports, movies, and lots of others. 

## Why Pantip Librarian?

At a glance, Pantip is quite friendly to simple web crawlers 
as it uses `unique number` in the URL to identify a particular 
thread. By changing this number, you simply access another topic.
This is super simple.

Pantip Librarian is a quick prototype of Q&A site crawler 
which scrapes the content of a range of topics on Pantip site 
and analyses the popularity factors over the scraped data.

## Prerequisites

Before running the tasks, these dependencies need to me met:

- [x] [Python 3.4+](https://www.python.org/download/releases/3.4.3/)
- [x] [Apache CouchDB](http://couchdb.apache.org/)
- [x] [Apache Spark](http://spark.apache.org/)
- [x] [Ruby 2.1+](https://www.ruby-lang.org/en/news/2015/08/18/ruby-2-1-7-released/)

## Prepare development environment

Suppose you have all major dependencies as listed in the previous 
section installed properly. Now you can simply run the script 
to install all development dependencies:

```bash
$ bash dev-setup.sh
```

The script basically collects and installs all Python libraries you 
need for running the library.

## Try it

`Pantip-Libr` is not a complex module so hopefully you can have a 
speedy first step. Following is the list of common tasks you can 
find.

### 1. Download Pantip threads

We have a script to fetch Pantip topics (in a specified range of IDs) 
and store them in a certain format in `CrouchDB` on your local machine. 
Simply run the following command:

```
$ python3 fetch.py
```

This would take some time to finish. The speed does depend on 
the quality of your Internet connection.

**Caveat**: Please accept my apology. The download script doesn't 
guard against HTTP connection failures. If network glitch happens, 
the script poorly ends execution.

### 2. Process the downloaded threads

This is still under development. By running the following command, 
you will potentially create a processing pipeline and have the entire 
downloaded thread data pushed into the processing queue.

```
$ python3 process.py
```

## Significant 3rd parties

These are our brilliant prerequisites.

- [x] [Thailang4r](https://github.com/veer66/thailang4r)
- [x] [Finch](https://github.com/jaimegildesagredo/finch) (Python REST consumer API)


## Licence

<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/80x15.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" property="dct:title">pantip-libr</span> by <span xmlns:cc="http://creativecommons.org/ns#" property="cc:attributionName">starcolon</span> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.

The module `pantip-libr` is distributed under 
Creative Commons 4.0 licence. Forking, modification, 
redistribution are welcome.

