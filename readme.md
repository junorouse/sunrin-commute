# sunrin-commute

Show the fastest way from "seoul bus transportation center" to sunrin internet highschool.  
It was created not to late for school.  

[http://sunrin.junoim.kr/](http://sunrin.junoim.kr/)

### Screenshot

![](http://i.imgur.com/CZC2rNV.jpg)

# install

```sh
cp sunrin-commute.conf /etc/init/sunrin-commute.conf
start sunrin-commute
cp sunrin-commute.nginx /etc/nginx/sites-available/sunrin-commute
ln -s /etc/nginx/sites-available/sunrin-commute /etc/nginx/sites-enabled/
service nginx restart
```
