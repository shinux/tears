# tears


> A bottle of Tears

[Demo](http://sinux.cc/)

**tears** (support Python3 only) is a pure clean blog, powered by bottle.
I love [next](https://github.com/iissnan/hexo-theme-next) cause you may found some dim shape of it's layout.

![](https://github.com/shnode/tears/raw/master/demo.png)


- tears keep simple and clean both in interface and backend, focus on content
- all backend code in one file to follow bottle's style
- posts with raw markdown files, just back up `source` folder periodically
- cantains a `post_engine` which check .md files and insert them into mongoDB
- work best in the latest desktop and mobile browsers(becuase bootstrap

## Usage

suppose you have mongodb installed in your system

```bash
    pip install -r requirements.txt
```

write your articles in /source

```bash
    python post_engine.py
    python tears.py
```

then access the url

```bash
    open "http://localhost:8080"
```

you may modify some personal information

## Contribute

Any advice is welcomed

## License
MIT
