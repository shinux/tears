# tears

**tears** (support Python3 only) is a pure clean blog, powered by bottle.
I love [next](https://github.com/iissnan/hexo-theme-next) cause you may found some dim shape of it's layout.

![](https://github.com/shnode/tears/raw/master/demo.png)


- tears keep simple and clean both in interface and backend, focus on content, 
- posts with raw markdown files, just back up `source` folder periodically. 
- cantains a `post_engine` which check .md files and insert them into mongoDB
- has good performance for mobile

## Usage

suppose you have mongodb installed in your system

```
    pip install -r requirements.txt
```
write your articles in /source 

```
    python post_engine.py
    python tears.py
```
then access the url

```
    open "http://localhost:8080"     
```
you may modify some personal information

## contribute

every fix and advice is welcomed

## License
MIT