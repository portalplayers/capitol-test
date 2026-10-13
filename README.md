# The Capitol Theatre: test website

Test version of the new website for The Capitol Theatre, owned and operated by Portal Players Dramatic Society, Port Alberni, BC.

- Plain HTML and CSS: no WordPress, no database.
- Published with GitHub Pages for board review.
- Every page tells search engines not to index it (`noindex` and `robots.txt`).

## Editing the site

The pages are generated from three files in `src/`:

- `src/build.py`: all page content and layout (shows, prices, links, text) and extra styles
- `src/seasons.py`: the Past Seasons list on the Our History page
- `src/base.css`: the main stylesheet

After editing, rebuild from the repository root, then commit and push:

```
python3 src/build.py            # test site (hidden from search engines)
NOINDEX=0 python3 src/build.py  # live site (visible to search engines)
```

Images live in `img/`. Don't edit the generated `.html` files or `site.css` directly; they are overwritten on every build.

Pages: home, What's On, 7 show pages, Season Pass, Tickets, Portal Players, Membership, Board & Governance, Our History, Helen Ford, Get Involved, Sponsor Our Season, Rentals, Visit & Contact.
