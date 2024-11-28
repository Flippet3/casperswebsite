### General info
Hello! I only made this repo public as a showcase of how my website was made.
Realistically it's not usable as a package or anything, but feel free to look around!

```src``` holds all of the code, where ```src/run_dashboard.py``` is the entry point. 
All panel configurations are in there, so it's run using a simple
```python run_dashboard.py```

The core of the website is the ```index.html```, which uses jinja2 syntax to allow for programmatic creation of cards and containers within bootstrap.
This is then leveraged using a base-class for a page in the website (in ```overview_base.py```).

Each page is made in ```src/dashboards/overviews```. Here classes inherit from the base and the pages can be made in a programmer friendly manner.
The reason for going through this length instead of using a simple backend/frontend set-up, is that this exposes the panel widgets.
These widgets are incredibly fast to set-up and offer wonderful interactivity in the browser, obscuring most of the boilerplate.

The website doesn't use much interactivity, but that is mostly because it doesn't need to. Extravagance for the sake of extravagance is... well... extravagant, if you ask me.
However, should the need ever arise, or if I'd like to create some silly page that showcases this, it should be a breeze to set-up.

### CI/CD
I've also set-up a workflow that allows every push to this repo to automatically be published to my little droplet server. Feel free to look, but it's nothing special.

### Testing
The astute of you might have noticed a distinct lack of testing, which I blame on the fact that I made this entire project in two/three days.
Also, I'd hardly call this website mission-critical, so I prefer a quick working environment with lots of trial and error (and eventually success) :))

Maybe I'll add some eventually to complete the showcase!