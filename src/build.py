#!/usr/bin/env python3
"""Builds the Concept C multi-page site for The Capitol Theatre into ./out"""
import os, html, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import seasons
HERE = os.path.dirname(os.path.abspath(__file__))
# Pages are written to the repository root (one level up from src/).
OUT = os.environ.get('SITE_OUT', os.path.dirname(HERE))
# Test site: hide from search engines. Set NOINDEX=0 for the live site.
NOINDEX = os.environ.get('NOINDEX', '1') != '0'
ROBOTS_META = '\n<meta name="robots" content="noindex, nofollow">' if NOINDEX else ''
# Live site only: public address, and the folder on the server it is uploaded to
# ("/" normally; "/new/" for the pre-launch test copy).
SITE_URL = 'https://atthecapitol.org/'
SITE_BASE = os.environ.get('SITE_BASE', '/')

E = html.escape

# ------------------------------------------------------------------ data
THUNDERTIX = 'https://portalplayersdramaticsociety.thundertix.com'
SEASON_URL = THUNDERTIX + '/packages'
MEMBER_URL = THUNDERTIX + '/memberships/89'
# Mailchimp signup form (same list as the old WordPress site's embedded form)
NEWS_URL = 'https://atthecapitol.us11.list-manage.com/subscribe/post?u=fc77e98ede9555f232ab4d968&amp;id=cce2b8cf41&amp;f_id=00a42fe0f0'
# Mailchimp's anti-spam field: must stay empty and hidden from people
NEWS_TRAP = '<div style="position:absolute;left:-5000px" aria-hidden="true"><input type="text" name="b_fc77e98ede9555f232ab4d968_cce2b8cf41" tabindex="-1" value=""></div>'
GCAL_URL = 'https://www.google.com/calendar/embed?src=dvpj1nslv2p13dk1gnjc5aslg8%40group.calendar.google.com&ctz=America/Vancouver'
MAP_URL = 'https://www.google.com/maps/search/?api=1&query=4904+Argyle+Street+Port+Alberni+BC'

EVENTS = [
    dict(slug='improv-comedy-rumble', kind='live', mon='Oct', day='23', range='Fri · 7:30 PM',
         long='Friday, October 23, 2026', time='7:30 PM', title='Improv Comedy Rumble',
         presenter='The Comedy Department', img='img/improv-rumble.jpg', thumb='',
         alt='The Comedy Department presents Improv Comedy Rumble',
         meta='Presented by The Comedy Department · "Whose Line Is It Anyway? meets the Thunderdome"',
         price='See ticket site', tix='https://www.thecomedydepartment.com/shows/port-alberni-bc-oct-23-2026/', tixvia='The Comedy Department',
         blurb=['No script. No rules. All comedy. Three improvisers go head to head in a comedy showdown the poster sums up as "Whose Line Is It Anyway? meets the Thunderdome."',
                'The Comedy Department performers have been seen with The Second City, Just for Laughs, CBC and Netflix.'],
         age=''),
    dict(slug='killer-bands-from-outer-space', kind='live', mon='Oct', day='25', range='Sun · 7:30 PM',
         long='Sunday, October 25, 2026', time='7:30 PM', title='Killer Bands from Outer Space',
         presenter='Punks On Port', img='img/punks-on-port.jpg', thumb='',
         alt='Punks On Port presents Killer Bands from Outer Space',
         meta='Presented by Punks On Port · Error=Human, The Fomites, Upstairs Neighbours, 0-1=2 · Halloween costume contest · Minors with a guardian',
         price='$15', tix=THUNDERTIX + '/events/272775', tixvia='ThunderTix',
         blurb=["Halloween's so nice you might as well do it twice. Punks On Port brings the wildest Halloween show in town: a multi-genre spectacle with a three-tier costume contest for Boils, Ghouls and Bands. So dress up!",
                'On the bill: Error=Human (industrial experimental, Port Alberni), The Fomites (horror and skate punk, Vancouver), Upstairs Neighbours (all-gal alt rock, Port Alberni), and 0-1=2, a tribute to Vancouver Island legends NoMeansNo, making their hometown debut.'],
         age='Minors welcome with a parent or guardian'),
    dict(slug='dreams-arrival', kind='live', mon='Nov', day='7', range='Sat · 7:30 PM',
         long='Saturday, November 7, 2026', time='7:30 – 9:30 PM', title='Dreams ~ Arrival',
         presenter='BMR Entertainment', img='img/dreams-arrival.webp', thumb='wide',
         alt='BMR Entertainment presents Dreams, the ultimate tribute to Fleetwood Mac, and Arrival, Canada\'s tribute to ABBA',
         meta='Presented by BMR Entertainment · Fleetwood Mac &amp; ABBA tribute concert',
         price='See Eventbrite', tix='https://www.eventbrite.ca/e/fleetwood-mac-abba-tribute-concert-with-dreams-arrival-port-alberni-tickets-1999981580746', tixvia='Eventbrite',
         blurb=['Dreams brings the songs of Fleetwood Mac and Arrival brings the hits of ABBA, back to back on one stage. A night of nostalgia, big harmonies and singalongs.',
                'The show runs about two hours. All sales are final, with no refunds.'],
         age=''),
    dict(slug='pen-pals', kind='pp', mon='Nov', day='13', range='to Nov 28',
         long='Fridays &amp; Saturdays, November 13–14, 20–21 &amp; 27–28, 2026', time='7:30 PM (box office opens 6:30 PM)', title='Pen Pals',
         presenter='Portal Players Dramatic Society', img='img/pen-pals.png', thumb='',
         alt='Pen Pals poster: two women writing letters, with airmail envelopes from Newark and Sheffield',
         meta='By Michael Griffo · 7:30 PM · $30 per person, or included in the $79 Season Pass', price='All seats $30 per person · or $79 Season Pass', tix=THUNDERTIX + '/events/266891', tixvia='ThunderTix',
         blurb=['<strong>Pen Pals</strong> by Michael Griffo.',
                'Pen Pals is the extraordinary story of two friends that unfolds over decades.',
                "Bernie and Mags live in two different countries. They've never met, and yet they're best friends, because they've been pen pals for over fifty years. Since they were teenagers, they've shared every aspect of their lives with each other: the trivial bits, the most intimate details, all the happiness, all the heartache. They've told each other things they wouldn't dare tell another soul. Even though Bernie lives in New Jersey and Mags is from England, the women are closer to each other than anyone else in the world.",
                '<strong>Come witness the journey of their lifetime. In their own words.</strong>',
                '<strong>Directed by</strong> Brent Ronning · <strong>Produced by</strong> Liane Fitzpatrick · <strong>Starring</strong> Katherine Hooton &amp; Alexandra Reynolds',
                '<em>Pen Pals is presented through special arrangement with Theatrical Rights Worldwide.</em>'], age=''),
    dict(slug='golden-anniversaries', kind='pp', mon='Feb', day='4', range='to Feb 20',
         long='February 4 – 20, 2027', time='7:30 PM', title='The Golden Anniversaries',
         presenter='Portal Players Dramatic Society', img='img/season-pass.jpg', thumb='crop c2',
         alt='The Golden Anniversaries artwork: a cake topped with a gold 50',
         meta='A comedy-drama about marriage, memory and long-term love · 7:30 PM · $30 per person, or included in the $79 Season Pass', price='$30 per person · or $79 Season Pass', tix=THUNDERTIX + '/events/266892', tixvia='ThunderTix',
         blurb=['<strong>Two people, one cottage, fifty years.</strong>',
                "Every year since they were married, Glen and Sandy Golden have been celebrating their wedding anniversary by coming to the same cottage on the lake for an annual weekend of quiet romance. And this year marks a major milestone: 50 years of wedded bliss. Well, mostly bliss&hellip; A week before the play begins, Sandy cancelled their big anniversary party and kicked Glen to the curb. And now, he wants to talk.",
                'Set over the course of one evening, as well as the past fifty years, the Goldens remember the good, the bad and the ugly of spending half a century together, and grapple with what comes next.',
                '<em>The Golden Anniversaries</em> is a comedy-drama about marriage, memory and long-term love.',
                '<strong>Written by</strong> Mark Crawford · <strong>Directed by</strong> Peter Wienold · <strong>Starring</strong> Liane Fitzpatrick &amp; Drew Waveryn',
                '<em>The Golden Anniversaries is produced by permission of the Playwright and Marquis Literary (Colin Rivers). <a href="https://www.MQlit.ca">www.MQlit.ca</a>.</em>'], age=''),
    dict(slug='comic-strippers', kind='live', mon='Feb', day='6', range='Sat',
         long='Saturday, February 6, 2027', time='7:30 – 9:30 PM', title='The Comic Strippers',
         presenter='The Roman Empire Production Corporation', img='img/comic-strippers.png', thumb='wide',
         alt='The Comic Strippers: a male stripper parody and improv comedy show',
         meta='Presented by The Roman Empire Production Corporation · A male stripper parody &amp; improv comedy show · 7:30 PM · 19+ only', price='See Eventbrite',
         tix='https://www.eventbrite.ca/e/the-comic-strippers-port-alberni-19only-tickets-2001900965678', tixvia='Eventbrite',
         blurb=["A male stripper parody and improv comedy show. Improv comedians play a fictitious male stripper troupe whose routines are gloriously unsexy, banter with the crowd and build scenes from audience suggestions.",
                'Winner of a Canadian Comedy Award for Best Live Production. Fun for all genders.',
                'The show runs about two hours. All sales are final, with no refunds.'],
         age='19+ only'),
    dict(slug='lips-together-teeth-apart', kind='pp', mon='Apr', day='15', range='to May 1',
         long='April 15 – May 1, 2027', time='7:30 PM', title='Lips Together, Teeth Apart',
         presenter='Portal Players Dramatic Society', img='img/season-pass.jpg', thumb='crop c3',
         alt='Lips Together, Teeth Apart artwork: two stacked teacups',
         meta='7:30 PM · $30 per person, or included in the $79 Season Pass', price='$30 per person · or $79 Season Pass', tix=THUNDERTIX + '/events/271202', tixvia='ThunderTix',
         blurb=["A gay community on Fire Island provides an unlikely setting for two straight couples, discovered lounging poolside and staring out to sea. Sally, married to Sam, a New Jersey contractor, has inherited the house from her brother, who died of AIDS. Sam's hyperkinetic sister Chloe and her smug, aristocratic husband John have come out for the Fourth of July weekend.",
                "Through monologues unheard by the others, the characters reveal a desperate sense of individual isolation. The only people these four find more alien are the gay men partying in the houses on either side of them. As they divert themselves from their own mortality with food, cocktails, The New York Times crossword, fireworks, charades and biting jabs at each other and the boys next door, Sally and Sam and John and Chloe find little to celebrate about themselves or their country on its birthday.",
                '<strong>Written by</strong> Terrence McNally · <strong>Directed by</strong> Diena Tyne', '<strong>Cast to be announced.</strong> Audition dates will be announced soon. Sign up for our newsletter at the bottom of this page to hear first, or see <a href="get-involved.html#propose">Auditions</a>.',
                '<em>LIPS TOGETHER, TEETH APART is presented by special arrangement with Broadway Licensing, LLC, servicing the Dramatists Play Service collection. (<a href="https://www.dramatists.com">dramatists.com</a>)</em>'], age=''),
]

NAV = [('whats-on.html', "What's On"), ('season.html', 'Season Pass'), ('portal-players.html', 'Portal Players'),
       ('get-involved.html', 'Get Involved'), ('rentals.html', 'Rentals'), ('visit.html', 'Visit')]

# ------------------------------------------------------------------ extra css for inner pages
EXTRA_CSS = r"""
.ns-float{position:fixed;top:0;left:0;right:0;z-index:60;display:flex;align-items:center;background:#0E0D13;border-top:1px solid #2E2D38;opacity:0;visibility:hidden;transform:translateY(-8px);transition:opacity .45s ease,transform .45s ease,visibility 0s linear .45s}
.ns-float.show{opacity:1;visibility:visible;transform:none;transition:opacity .45s ease,transform .45s ease,visibility 0s}
.ns-float form{display:flex;align-items:center;justify-content:center;gap:10px;width:100%}
.ns-float label{font-family:var(--serif);font-weight:700;font-size:17px;color:#F3EEE4;white-space:nowrap;margin-right:4px}
.ns-float .nf-short{display:none}
.ns-float input{font:inherit;font-size:14px;width:220px;min-width:0;height:32px;padding:0 10px;border:1px solid #3A3846;border-radius:2px;background:#1E1D26;color:#F3EEE4}
.ns-float input::placeholder{color:#8E8778}
.ns-float input:focus{outline:2px solid var(--amber);outline-offset:1px;border-color:var(--amber)}
.ns-float button{font:700 13px var(--sans);height:32px;padding:0 14px;border:0;border-radius:2px;background:var(--amber);color:var(--dark);cursor:pointer;white-space:nowrap}
@media (max-width:620px),(max-height:500px) and (orientation:landscape){
  .ns-float .nf-long{display:none}.ns-float .nf-short{display:inline}
  .ns-float label{font:700 12px var(--sans);letter-spacing:.04em}
  .ns-float form{gap:8px}
  .ns-float input{flex:1 1 auto;width:auto;max-width:260px;height:28px;font-size:13px}
  .ns-float button{height:28px;font-size:12px;padding:0 12px}
}
@media (prefers-reduced-motion:reduce){.ns-float,.ns-float.show{transition:none;transform:none}}


.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}
.news-strip{background:var(--dark);color:#F3EEE4;padding:30px 0}
.news-strip .wrap{display:flex;align-items:center;justify-content:space-between;gap:20px 40px;flex-wrap:wrap}
.news-strip h2{font-size:clamp(24px,2.6vw,32px);color:#F3EEE4}
.news-strip p{margin:4px 0 0;color:#BFB4A3;font-size:16px}
.news-strip form{display:flex;gap:10px;flex:0 1 460px;flex-wrap:wrap}
.news-strip input{font:inherit;flex:1 1 220px;min-width:0;width:100%;min-height:48px;padding:0 14px;border:1px solid #3A3846;border-radius:2px;background:#1E1D26;color:#F3EEE4}
.news-strip input::placeholder{color:#8E8778}
.news-strip input:focus{outline:2px solid var(--amber);outline-offset:1px;border-color:var(--amber)}
.news-strip button{font:700 16px var(--sans);min-height:48px;padding:0 24px;border:0;border-radius:2px;background:var(--amber);color:var(--dark);cursor:pointer}
@media (max-width:520px){.news-strip form{flex-basis:100%;min-width:0}.news-strip input{flex-basis:100%}.news-strip button{flex:1 1 100%}}

footer a.soc-link{display:flex;align-items:center;gap:8px}
.soc{width:16px;height:16px;flex:0 0 16px;opacity:.85}
footer a.soc-link:hover .soc{opacity:1}
/* centre the hero "Next on stage" ticket when it drops below the text */
@media (max-width:960px){.hero-c .ticket{margin-left:auto;margin-right:auto}}
/* phones held sideways: keep the pinned bar slim */
@media (max-height:500px) and (orientation:landscape){
  nav.sticky-nav ul{flex-wrap:nowrap;justify-content:flex-start;overflow-x:auto;padding:0 8px;scrollbar-width:none}
  nav.sticky-nav li:first-child{margin-left:auto}
  nav.sticky-nav li:last-child{margin-right:auto}
  nav.sticky-nav ul::-webkit-scrollbar{display:none}
  nav.sticky-nav a{padding:10px 8px;font-size:11px;letter-spacing:.08em;white-space:nowrap}
  nav.sticky-nav a.tix{padding:5px 12px;margin:5px 4px}
  .nav-strip .mini-news{display:none!important}
  .nav-strip .wrap{justify-content:center;padding-top:4px;padding-bottom:4px}
  .mini-news-link{display:inline-block!important;font:700 12px var(--sans);letter-spacing:.04em;color:var(--amber);border:1px solid var(--amber);padding:3px 12px;border-radius:2px;text-decoration:none}
  [id]{scroll-margin-top:84px}
}
a.thumb{display:block;transition:transform .15s,box-shadow .15s}
a.thumb:hover{transform:translateY(-2px);box-shadow:0 8px 18px rgba(0,0,0,.25)}
.map-band{position:relative;height:240px;background:#2A2D3A;border-bottom:1px solid var(--rule)}
.map-band iframe{display:block;width:100%;height:100%;border:0;filter:grayscale(.25) contrast(1.05)}
.map-link{position:absolute;inset:0;display:flex;align-items:flex-end;justify-content:center;padding:16px;text-decoration:none}
.map-link span{background:var(--dark);color:#F3EEE4;font-weight:700;font-size:15px;padding:10px 18px;border-radius:3px;box-shadow:0 6px 16px rgba(0,0,0,.3)}
.map-link:hover span,.map-link:focus-visible span{background:var(--amber);color:var(--dark)}
@media (max-width:620px){.map-band{height:190px}.map-link span{font-size:13px;padding:8px 12px;text-align:center}}
.sponsor-band{margin-top:36px;padding-top:24px;border-top:1px solid #2E2D38;text-align:center;--g:clamp(8px,3vw,40px);--t:min(108px,calc((100vw - 48px - 3 * var(--g)) / 6.62))}
.sb-head{font-family:var(--display);font-weight:700;font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:#BFB4A3;margin-bottom:16px}
.sb-row{display:flex;flex-wrap:nowrap;justify-content:center;align-items:center;gap:var(--g)}
.sb-row .sp-logo{flex:0 0 auto;width:auto;height:var(--t);padding:calc(var(--t) * .1);background:#FFFFFF;border-radius:3px;opacity:1;box-sizing:border-box}
.sb-row .sp-logo img{display:block;height:100%;width:auto;max-width:none;max-height:none}
.sb-row .sp-logo.flush{padding:0;background:none;border-radius:0}
.sp-row.light .sp-logo.flush{padding:0;border:0;background:none}
.sb-more{display:inline-block;margin-top:14px;font-size:13px;color:var(--amber)!important;padding:0}
.foot-extra{display:flex;flex-wrap:wrap;gap:28px 48px;align-items:flex-end;justify-content:space-between;margin-top:40px}
.foot-extra .member-badge{margin-top:0}
.sp-row{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin-bottom:10px}
.sp-logo{display:flex;align-items:center;justify-content:center;width:112px;height:60px;background:#FFFFFF;border-radius:3px;padding:6px;opacity:.88;transition:opacity .15s}
.sp-logo:hover{opacity:1}
.sp-logo img{max-width:100%;max-height:100%;width:auto;height:auto;object-fit:contain}
.sp-row.light .sp-logo{background:#fff;border:1px solid var(--rule);opacity:1}
.member-badge{display:inline-flex;align-items:center;gap:16px;margin-top:36px;text-decoration:none;color:#C9C3B8}
.member-badge img{width:72px;height:72px;flex:0 0 72px}
.member-badge b{display:block;font-family:var(--display);font-size:14px;letter-spacing:.12em;text-transform:uppercase;color:#F3EEE4}
.member-badge small{display:block;font-size:13px;margin-top:4px}
.member-badge:hover b{color:var(--amber)}
.foot-map{margin:12px 0 8px;border:1px solid #3A3846;border-radius:3px;overflow:hidden;max-width:300px}
.foot-map iframe{display:block;width:100%;height:150px;border:0;filter:grayscale(.35) contrast(1.05)}
.roles{columns:3;column-gap:28px}
@media (max-width:620px){.roles{columns:2}}
/* sticky main menu */
.top .masthead{padding-bottom:14px}
.sticky-bar{position:sticky;top:0;z-index:50;box-shadow:0 6px 18px rgba(0,0,0,.28)}
.nav-strip{background:#0E0D13;border-top:1px solid #2E2D38}
.nav-strip .wrap{display:flex;justify-content:center;align-items:center;padding-top:6px;padding-bottom:6px}
.mini-news-link{display:none}
@media (max-width:620px){.nav-strip .mini-news{display:none}.nav-strip .wrap{justify-content:center;padding-top:5px;padding-bottom:5px}.mini-news-link{display:inline-block;font:700 12px var(--sans);letter-spacing:.04em;color:var(--amber);border:1px solid var(--amber);padding:4px 12px;border-radius:2px;text-decoration:none}}
nav.main.sticky-nav{margin:0;background:var(--dark);border-top:1px solid #3A3846;border-bottom:1px solid #3A3846}
nav.sticky-nav a{color:#F3EEE4}
nav.sticky-nav a:hover{color:var(--amber)}
nav.sticky-nav a[aria-current="page"]{color:var(--amber)}
nav.sticky-nav a.tix{background:var(--amber);color:var(--dark);margin:6px 0 6px 8px;padding:8px 18px;border-radius:2px}
nav.sticky-nav a.tix:hover{background:#F6D58E;color:var(--dark)}
[id]{scroll-margin-top:112px}
@media (max-width:760px){
  nav.sticky-nav ul{flex-wrap:nowrap;justify-content:flex-start;overflow-x:auto;padding:0 8px;scrollbar-width:none}
  nav.sticky-nav ul::-webkit-scrollbar{display:none}
  nav.sticky-nav ul{-webkit-mask-image:linear-gradient(90deg,#000 82%,transparent);mask-image:linear-gradient(90deg,#000 82%,transparent)}
  nav.sticky-nav a{padding:12px 10px;font-size:12px;white-space:nowrap}
  nav.sticky-nav a.tix{padding:6px 12px;margin:6px 4px}
}
.util-right{display:flex;flex-direction:column;align-items:flex-end;gap:8px}
.mini-news{display:flex;align-items:center;gap:8px;flex-wrap:wrap;font-size:13px}
.mini-news label{color:#BFB4A3}
.mini-news input{font:inherit;font-size:13px;width:170px;min-height:32px;padding:4px 10px;border:1px solid #3A3846;border-radius:2px;background:#1E1D26;color:#F3EEE4}
.mini-news input::placeholder{color:#8E8778}
.mini-news input:focus{outline:2px solid var(--amber);outline-offset:1px;border-color:var(--amber)}
.mini-news button{font:700 13px var(--sans);min-height:32px;padding:4px 12px;border:1px solid var(--amber);border-radius:2px;background:transparent;color:var(--amber);cursor:pointer}
.mini-news button:hover{background:var(--amber);color:var(--dark)}

/* ===== full site additions ===== */
.skip{position:absolute;left:-9999px;top:0;background:var(--amber);color:var(--dark);padding:10px 16px;z-index:10;font-weight:700}
.skip:focus{left:16px;top:16px}
nav.main a[aria-current="page"]{color:var(--amber)}
.page-head{position:relative;overflow:hidden;background:var(--dark);color:#F3EEE4;padding:56px 0 64px;border-top:1px solid #2E2D38}
.page-head .bg{position:absolute;top:0;right:0;width:55%;height:100%;object-fit:cover;opacity:.18;filter:sepia(.5)}
.page-head .shade{position:absolute;inset:0;background:linear-gradient(90deg,var(--dark) 40%,rgba(20,19,26,.6) 100%)}
.page-head .wrap{position:relative}
.crumbs{font-size:14px;color:#BFB4A3;margin-bottom:14px}
.crumbs a{color:#BFB4A3}
.page-head .eyebrow{color:var(--amber)}
.page-head h1{font-family:var(--serif);font-size:clamp(38px,5.4vw,64px);margin-top:10px;line-height:1.05}
.page-head p.sub{font-size:20px;color:#DDD7CC;max-width:680px;margin:18px 0 0}
.layout{display:flex;flex-wrap:wrap;gap:48px;align-items:flex-start}
.layout .main{flex:999 1 560px;min-width:0}
.layout aside{flex:1 1 300px;min-width:0;max-width:420px}
.prose{max-width:760px}
.prose h2{font-size:clamp(28px,3.2vw,38px);margin:48px 0 14px}
.prose h2:first-child{margin-top:0}
.prose h3{font-size:22px;margin:28px 0 8px}
.prose p{margin:0 0 16px;color:var(--ink-2)}
.prose ul{margin:0 0 16px;padding-left:22px;color:var(--ink-2)}
.prose li{margin-bottom:6px}
.prose strong{color:var(--ink)}
.note{background:var(--paper-2);border-left:4px solid var(--gold);padding:16px 20px;margin:20px 0;font-size:16px;color:var(--ink-2)}
.box{background:#fff;border:1px solid var(--rule);padding:28px;display:flex;flex-direction:column;gap:12px}
.box h3{font-size:22px}
.box p{margin:0;color:var(--ink-2);font-size:16px}
.box dl{margin:0;display:grid;grid-template-columns:auto 1fr;gap:6px 14px;font-size:16px}
.box dt{font-weight:700}
.box dd{margin:0;color:var(--ink-2)}
.box.dark{background:var(--dark);color:#F3EEE4;border-color:var(--dark)}
.box.dark p,.box.dark dd{color:#C9C3B8}
.box.dark a{color:var(--amber)}
.stack{display:flex;flex-direction:column;gap:20px}
.cards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px}
.cards.two{grid-template-columns:repeat(2,minmax(0,1fr))}
.cards.four{grid-template-columns:repeat(4,minmax(0,1fr))}
@media (max-width:980px){.cards,.cards.four{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:620px){.cards,.cards.two,.cards.four{grid-template-columns:1fr}}
.people{width:100%;border-collapse:collapse;font-size:17px}
.people th,.people td{text-align:left;padding:12px 10px;border-bottom:1px solid var(--rule);vertical-align:top}
.people th{font-family:var(--display);font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:var(--red);font-weight:700}
.table-box{overflow-x:auto}
.docs{list-style:none;margin:0;padding:0;border-top:1px solid var(--rule)}
.docs li{display:flex;flex-wrap:wrap;gap:8px 20px;justify-content:space-between;align-items:center;padding:16px 0;border-bottom:1px solid var(--rule)}
.docs b{font-family:var(--serif);font-size:19px;display:block}
.docs span{font-size:15px;color:var(--ink-2)}
.form{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px 20px}
.form label{display:flex;flex-direction:column;gap:6px;font-weight:700;font-size:15px}
.form .full{grid-column:1/-1}
.form input,.form select,.form textarea{font:inherit;font-weight:400;min-height:48px;padding:10px 14px;border:1.5px solid var(--ink);border-radius:2px;background:#fff;color:var(--ink)}
.form textarea{min-height:130px}
@media (max-width:620px){.form{grid-template-columns:1fr}}
.show-hero{background:var(--dark);color:#F3EEE4;padding:48px 0 64px;border-top:1px solid #2E2D38}
.show-hero .wrap{display:flex;flex-wrap:wrap;gap:48px;align-items:flex-start}
.show-hero .poster{flex:1 1 340px;min-width:0;max-width:460px}
.show-hero .poster img{box-shadow:0 22px 44px rgba(0,0,0,.5);border-radius:3px}
.show-hero .poster .crop-box{aspect-ratio:458/490;overflow:hidden;border-radius:3px;box-shadow:0 22px 44px rgba(0,0,0,.5)}
.show-hero .poster .crop-box img{width:300%;max-width:none;margin-top:-61%;box-shadow:none}
.show-hero .poster .crop-box.c2 img{margin-left:-100%}
.show-hero .poster .crop-box.c3 img{margin-left:-200%}
.show-hero .details{flex:999 1 440px;min-width:0}
.show-hero h1{font-family:var(--serif);font-size:clamp(40px,5.4vw,68px);line-height:1.02;margin:16px 0 0}
.show-hero .by{font-size:19px;color:#DDD7CC;margin-top:10px}
.show-hero .tag-live{border-color:#F3EEE4;color:#F3EEE4}
.facts-row{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));margin:30px 0 0;border:1px solid #3A3846;border-radius:4px}
.facts-row div{padding:16px 18px;border-right:1px solid #3A3846}
.facts-row div:last-child{border-right:0}
.facts-row dt{font-family:var(--display);font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:#BFB4A3;font-weight:700}
.facts-row dd{margin:6px 0 0;font-family:var(--serif);font-size:20px;line-height:1.25}
@media (max-width:620px){.facts-row{grid-template-columns:1fr}.facts-row div{border-right:0;border-bottom:1px solid #3A3846}.facts-row div:last-child{border-bottom:0}}
.show-hero .ctas{display:flex;flex-wrap:wrap;gap:14px;align-items:center;margin-top:26px}
.show-hero .ctas small{color:#BFB4A3;font-size:14px}
.ph{background:#FFF4D6;padding:0 4px;border-radius:2px}
"""

# ------------------------------------------------------------------ chrome
def header(active):
    links = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == active else ''
        links.append(f'<li><a href="{href}"{cur}>{label}</a></li>')
    links.append('<li><a class="tix" href="tickets.html">Buy Tickets</a></li>')
    return f'''<a class="skip" href="#content">Skip to content</a>
<div class="top">
<div class="utility">
  <div class="wrap">
    <div class="lines"><span>Box office opens one hour before every Portal Players production</span><span>Cash, debit, Mastercard &amp; Visa</span></div>
    <div class="util-right">
    <div class="contact"><a href="tel:2507231195">250-723-1195</a><a href="mailto:capitoltheatre@shaw.ca">capitoltheatre@shaw.ca</a></div>
    </div>
  </div>
</div>
<header class="masthead">
  <div class="wrap">
    <a href="index.html" style="text-decoration:none"><div class="name">The Capitol Theatre</div>
    <div class="society">Portal Players Dramatic Society</div></a>
    <div class="ornament" aria-hidden="true">✦ &nbsp;Port Alberni · Since 1936&nbsp; ✦</div>
  </div>
  <div class="bulbs" aria-hidden="true"></div>
</header>
</div>
<div class="sticky-bar">
<div class="nav-strip"><div class="wrap">
    <form class="mini-news" action="{NEWS_URL}" method="post" target="_blank" aria-label="Newsletter signup">{NEWS_TRAP}
      <label for="mini-email">Subscribe to our Newsletter</label>
      <input id="mini-email" type="email" name="EMAIL" placeholder="you@example.com" required>
      <button type="submit">Sign up</button>
    </form>
    <a class="mini-news-link" href="#newsletter">Subscribe to our Newsletter</a>
</div></div>
<nav class="main sticky-nav" aria-label="Main">
  <ul>
    {''.join(links)}
  </ul>
</nav>
</div>
'''

FOOTER = f'''<section class="news" id="newsletter">
  <div class="wrap">
    <h2>Subscribe to our Newsletter</h2>
    <p>New shows, auditions and presales, straight to your inbox.</p>
    <form action="{NEWS_URL}" method="post" target="_blank">{NEWS_TRAP}
      <label>Email address<input type="email" name="EMAIL" placeholder="you@example.com" required></label>
      <button type="submit">Subscribe</button>
    </form>
  </div>
</section>
<footer>
  <div class="wrap">
    <div class="cols">
      <div><div class="h">The Capitol Theatre</div>4904 Argyle Street<br>Port Alberni, BC V9Y 1V7
        <div class="foot-map"><iframe title="Map showing The Capitol Theatre, 4904 Argyle Street, Port Alberni" src="https://www.google.com/maps?q=Capitol+Theatre,+4904+Argyle+Street,+Port+Alberni,+BC&amp;z=15&amp;output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
        <a href="{MAP_URL}" style="font-weight:700">Get directions →</a><a href="visit.html" style="font-weight:700">Plan your visit →</a></div>
      <div><div class="h">Box office</div>Opens one hour before every Portal Players production<br>250-723-1195<br><a href="mailto:capitoltheatre@shaw.ca" style="display:inline;padding:0">capitoltheatre@shaw.ca</a></div>
      <nav aria-label="About Portal Players"><div class="h">Portal Players</div><a href="portal-players.html">Who we are</a><a href="membership.html">Membership</a><a href="board.html">Board &amp; governance</a><a href="history.html">Our history</a><a href="helen-ford.html">Helen Ford</a><a class="soc-link" href="https://www.facebook.com/groups/10278245586"><svg class="soc" viewBox="0 0 24 24" aria-hidden="true"><circle cx="9" cy="8.5" r="3.2" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M3 19.5c.6-3.3 3-5.2 6-5.2s5.4 1.9 6 5.2" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><path d="M15.8 5.6a3 3 0 0 1 0 5.8M17.6 14.6c1.7.7 2.9 2.4 3.3 4.9" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>Members' Facebook group</a></nav>
      <nav aria-label="More"><div class="h">More</div><a href="tickets.html">Tickets</a><a href="get-involved.html">Volunteer &amp; donate</a><a href="sponsor.html">Sponsor our season</a><a href="rentals.html">Rent the theatre</a><a href="visit.html#contact">Contact us</a><a class="soc-link" href="https://www.facebook.com/CapitolTheatrePortAlberni"><svg class="soc" viewBox="0 0 24 24" aria-hidden="true"><rect x="2" y="2" width="20" height="20" rx="4.5" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M15.5 7.5h-1.8c-1.6 0-2.4.9-2.4 2.5V12H9.5v2.6h1.8V21h2.8v-6.4h2.1l.4-2.6h-2.5v-1.6c0-.6.3-.9.9-.9h1.6z" fill="currentColor"/></svg>Facebook</a><a class="soc-link" href="https://www.instagram.com/at.the.capitol.theatre/"><svg class="soc" viewBox="0 0 24 24" aria-hidden="true"><rect x="2.5" y="2.5" width="19" height="19" rx="5.5" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="12" r="4.2" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="17.4" cy="6.6" r="1.2" fill="currentColor"/></svg>Instagram</a><a class="soc-link" href="https://www.youtube.com/@PortalPlayers"><svg class="soc" viewBox="0 0 24 24" aria-hidden="true"><rect x="1.8" y="5" width="20.4" height="14" rx="4" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M10 8.9v6.2l5.4-3.1z" fill="currentColor"/></svg>YouTube</a></nav>
    </div>
    <div class="foot-extra">
    <a class="member-badge" href="https://www.theatrebc.org" target="_blank" rel="noopener">
      <img src="img/theatre-bc.png" alt="Theatre BC logo" width="72" height="72" loading="lazy">
      <span><b>Proud member of Theatre BC</b><small>Promoting the development of theatre in B.C. since 1932 · theatrebc.org</small></span>
    </a>
    </div>
    <div class="sponsor-band">
      <div class="sb-head">Thank you to our marquee sponsors</div>
      <div class="sb-row"><a class="sp-logo flush" href="https://www.thegraphicsfactory.com" target="_blank" rel="noopener"><img src="img/sponsor-graphics-factory.png" alt="Graphics Factory Printing &amp; Signs" loading="lazy"></a><span class="sp-logo"><img src="img/sponsor-coop.png" alt="Alberni District Co-op" loading="lazy"></span><a class="sp-logo" href="https://dbasilencing.ca" target="_blank" rel="noopener"><img src="img/sponsor-dba.png" alt="DBA Metal Art" loading="lazy"></a><span class="sp-logo"><img src="img/sponsor-tpa.png" alt="Tim Pley &amp; Associates" loading="lazy"></span></div>
      <a class="sb-more" href="sponsor.html">Become a sponsor →</a>
    </div>
    <div class="legal">© Portal Players Dramatic Society · The Alberni Valley's community theatre · A registered charity and non-profit society that owns and operates The Capitol Theatre<br>Charitable registration no. 89081 5442 RR0001 · BC Society No. S-24357</div>
  </div>
</footer>
'''

FILTER_JS = '''<script>
(function(){
  var btns=document.querySelectorAll('.filters button');
  btns.forEach(function(b){
    b.addEventListener('click',function(){
      var f=b.getAttribute('data-f');
      btns.forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});
      document.querySelectorAll('.event').forEach(function(e){
        e.style.display=(f==='all'||e.classList.contains(f))?'':'none';
      });
    });
  });
})();
</script>'''

import hashlib
CSS_VER = hashlib.sha1((open(os.path.join(HERE,'base.css')).read()).encode()).hexdigest()[:8]


import re as _re
def smarten(html_text):
    """Curly quotes and apostrophes in visible text only (not tags, scripts or styles)."""
    out=[]; skip=False
    for part in _re.split(r'(<[^>]+>)', html_text):
        if part.startswith('<'):
            low=part.lower()
            if low.startswith('<script') or low.startswith('<style'): skip=True
            elif low.startswith('</script') or low.startswith('</style'): skip=False
            out.append(part); continue
        if skip or not part: out.append(part); continue
        t=part.replace('&#39;',"'").replace('&quot;','"')
        t=_re.sub(r"(\w)'(\w)", "\\1\u2019\\2", t)          # apostrophes in words
        t=_re.sub(r"(^|[\s(\[\u2014\u2013-])'", "\\1\u2018", t)  # opening single
        t=t.replace("'", "\u2019")                                     # closing single / leftover
        t=_re.sub(r'(^|[\s(\[\u2014\u2013-])"', "\\1\u201c", t)  # opening double
        t=t.replace('"', "\u201d")                                     # closing double
        out.append(t)
    return ''.join(out)

import re as _re
def clean_links(doc):
    """Link to pages without ".html" (e.g. visit.html#contact -> visit#contact; index.html -> ./)."""
    def fix(m):
        name, anchor = m.group(1), m.group(2) or ''
        return f'href="{"./" if name == "index" else name}{anchor}"'
    return _re.sub(r'href="([a-z0-9-]+)\.html(#[^"]*)?"', fix, doc)

def page(fname, title, desc, active, body, js='', base=False):
    canon = '' if NOINDEX else '\n<link rel="canonical" href="' + SITE_URL + ('' if fname == 'index.html' else fname[:-5]) + '">'
    basetag = f'\n<base href="{SITE_BASE}">' if base else ''
    doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">{ROBOTS_META}{basetag}
<title>{title}</title>{canon}
<meta name="description" content="{E(desc)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@800;900&family=Cinzel:wght@500;700;800&family=Libre+Caslon+Text:ital,wght@0,400;0,700;1,400&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="site.css?v={CSS_VER}">
</head>
<body>
{header(active)}
<main id="content">
{body}
</main>
{FOOTER}
{js}
</body>
</html>
'''
    open(os.path.join(OUT, fname), 'w').write(clean_links(smarten(doc)))

def page_head(eyebrow, h1, sub='', crumbs=None, bg=True):
    c = ''
    if crumbs:
        c = '<div class="crumbs"><a href="index.html">Home</a>' + ''.join(
            f' / <a href="{h}">{t}</a>' if h else f' / {t}' for h, t in crumbs) + '</div>'
    bgimg = '<img class="bg" src="img/opening-day-1936.png" alt="" aria-hidden="true"><div class="shade" aria-hidden="true"></div>' if bg else ''
    s = f'<p class="sub">{sub}</p>' if sub else ''
    return f'''<section class="page-head">{bgimg}<div class="wrap">{c}<div class="eyebrow">{eyebrow}</div><h1>{h1}</h1>{s}</div></section>'''

def tag(kind):
    return '<span class="tag tag-pp">Portal Players Presents</span>' if kind == 'pp' else '<span class="tag tag-live">Live at the Capitol</span>'

def event_row(ev):
    btn = 'btn-solid' if ev['kind'] == 'pp' else 'btn-line'
    age = f' <span class="age">19+</span>' if ev['age'] == '19+ only' else ''
    return f'''      <li class="event {ev['kind']}">
        <div class="date"><span class="m">{ev['mon']}</span><span class="d">{ev['day']}</span><span class="r">{ev['range']}</span></div>
        <a class="thumb {ev['thumb']}" href="show-{ev['slug']}.html" tabindex="-1" aria-hidden="true"><img src="{ev['img']}" alt="" loading="lazy"></a>
        <div class="info">{tag(ev['kind'])}<h3><a href="show-{ev['slug']}.html" style="color:inherit;text-decoration:none">{ev['title']}</a>{age}</h3><div class="meta">{ev['meta']}</div></div>
        <a class="btn {btn}" href="show-{ev['slug']}.html">Tickets &amp; info</a>
      </li>'''

def events_block(head_html):
    rows = '\n'.join(event_row(e) for e in EVENTS)
    return f'''<section class="block" id="whats-on">
  <div class="wrap">
    <div class="head">
      {head_html}
      <div class="filters" role="group" aria-label="Filter shows">
        <button type="button" aria-pressed="true" data-f="all">All shows</button>
        <button type="button" aria-pressed="false" data-f="pp">Portal Players productions</button>
        <button type="button" aria-pressed="false" data-f="live">Visiting shows</button>
      </div>
    </div>
    <ol class="events">
{rows}
    </ol>
  </div>
</section>'''

SEASON_BLOCK = f'''<section class="season" id="season">
  <div class="wrap">
    <div class="eyebrow">Portal Players Presents · 2026–27 Season Pass</div>
    <h2>Three shows. One great season.</h2>
    <p class="lead">Your neighbours, on our own stage. The Season Pass gets you into one performance of each Portal Players production this year.</p>
    <div class="trio">
      <a class="play" href="show-pen-pals.html" style="text-decoration:none"><div class="art"><img src="img/pen-pals.png" alt="Pen Pals poster" style="width:100%;height:100%;margin:0;object-fit:cover;object-position:top"></div><h3>Pen Pals</h3><p>November 13 – 28, 2026</p></a>
      <a class="play c2" href="show-golden-anniversaries.html" style="text-decoration:none"><div class="art"><img src="img/season-pass.jpg" alt="The Golden Anniversaries artwork: a cake topped with a gold 50"></div><h3>The Golden Anniversaries</h3><p>February 4 – 20, 2027</p></a>
      <a class="play c3" href="show-lips-together-teeth-apart.html" style="text-decoration:none"><div class="art"><img src="img/season-pass.jpg" alt="Lips Together, Teeth Apart artwork: two stacked teacups"></div><h3>Lips Together, Teeth Apart</h3><p>April 15 – May 1, 2027</p></a>
    </div>
    <div class="stub">
      <div class="price"><span>Season Pass</span><strong>$79</strong></div>
      <div class="terms">
        <p>One performance of each production. Buy your season now and choose your dates and seats later.</p>
        <div class="actions"><a class="btn btn-solid" href="{SEASON_URL}">Buy the Season Pass</a><a class="btn btn-line" href="tickets.html">Single show tickets</a></div>
      </div>
    </div>
  </div>
</section>'''

NEWS_STRIP = f'''<section class="news-strip" aria-label="Newsletter signup">
  <div class="wrap">
    <div class="ns-text"><h2>Subscribe to our Newsletter</h2><p>New shows, auditions and presales, straight to your inbox.</p></div>
    <form action="{NEWS_URL}" method="post" target="_blank">{NEWS_TRAP}
      <label for="strip-email" class="sr-only">Email address</label>
      <input id="strip-email" type="email" name="EMAIL" placeholder="Your email" required>
      <button type="submit">Subscribe</button>
    </form>
  </div>
</section>
<div class="ns-float" aria-hidden="true" inert>
  <form class="wrap" action="{NEWS_URL}" method="post" target="_blank">{NEWS_TRAP}
    <label for="float-email"><span class="nf-long">Subscribe to our Newsletter</span><span class="nf-short">Newsletter</span></label>
    <input id="float-email" type="email" name="EMAIL" placeholder="Your email" required>
    <button type="submit">Subscribe</button>
  </form>
</div>'''

STRIP_JS = '''<script>
(function(){
  var band=document.querySelector('.news-strip'), fl=document.querySelector('.ns-float'),
      bar=document.querySelector('.sticky-bar'), ns=document.querySelector('.nav-strip');
  if(!band||!fl||!bar||!ns) return;
  var on=false, ticking=false;
  function update(){
    ticking=false;
    fl.style.height=ns.offsetHeight+'px';
    var past=band.getBoundingClientRect().bottom < bar.getBoundingClientRect().bottom;
    var show=past;
    if(show!==on){
      on=show;
      fl.classList.toggle('show',show);
      if(show){fl.removeAttribute('aria-hidden');fl.removeAttribute('inert');}
      else{fl.setAttribute('aria-hidden','true');fl.setAttribute('inert','');}
    }
  }
  function req(){ if(!ticking){ticking=true;requestAnimationFrame(update);} }
  window.addEventListener('scroll',req,{passive:true});
  window.addEventListener('resize',req);
  update();
})();
</script>'''

SP = 'Partner with Portal Players and turn our promotion into your promotion. Six partnership packages, from $120 for individuals to $3,000+ for businesses, with season tickets, logos, programme ads and more.'
INVOLVE_BLOCK = f'''<section class="block" id="involve">
  <div class="wrap">
    <div class="head"><div><div class="eyebrow">Every seat, light and curtain is volunteer-powered</div><h2>Keep the lights on</h2></div></div>
    <div class="trio-text">
      <div><div class="n">I</div><h3>Become a member</h3><p>Join Portal Players Dramatic Society, vote at the AGM and be first to hear about auditions.</p><a href="membership.html">Join Portal Players →</a></div>
      <div><div class="n">II</div><h3>Volunteer</h3><p>Act, direct, run lights and sound, build sets or welcome the audience at front of house. No experience needed.</p><a href="get-involved.html#volunteer">Find your role →</a></div>
      <div><div class="n">III</div><h3>Sponsor Our Season</h3><p>{SP}</p><a href="sponsor.html">See partnership packages →</a></div>
      <div><div class="n">IV</div><h3>Donate</h3><p>Portal Players is a registered charity. Your gift keeps a 90-year-old building alive, and we issue official tax receipts.</p><a href="get-involved.html#donate">Give today →</a></div>
    </div>
  </div>
</section>'''

VISIT_BOX = f'''<div class="box dark">
  <div class="eyebrow" style="color:var(--amber)">Plan your visit</div>
  <dl>
    <dt>Where</dt><dd>4904 Argyle Street, Port Alberni</dd>
    <dt>Box office</dt><dd>Opens one hour before every Portal Players production. Cash, debit, Mastercard &amp; Visa.</dd>
    <dt>Parking</dt><dd>Street parking on Argyle Street, 4th Avenue and nearby streets</dd>
    <dt>Access</dt><dd>Ramp to the main lobby doors on Argyle Street</dd>
    <dt>Call</dt><dd><a href="tel:2507231195">250-723-1195</a></dd>
  </dl>
  <a href="visit.html"><b>More visitor info →</b></a>
</div>'''

# ------------------------------------------------------------------ pages
def build_home():
    nxt = EVENTS[0]
    body = f'''<section class="hero-c">
  <img class="bg" src="img/opening-day-1936.png" alt="" aria-hidden="true">
  <div class="shade" aria-hidden="true"></div>
  <div class="wrap">
    <div class="copy">
      <div class="eyebrow">4904 Argyle Street · Port Alberni</div>
      <h1>Live on Argyle Street <em>since 1936.</em></h1>
      <p class="lede">This historic former movie theatre is now home of the performing arts, owned and operated by <strong>Portal Players Dramatic Society</strong>. Our team of volunteers produce and perform plays and musicals at The Capitol Theatre. When we're not on stage with our own productions, doors are open to touring acts, concerts and local events.</p>
      <div class="ctas">
        <a class="btn btn-amber" href="whats-on.html">See what's on</a>
        <a class="btn btn-ghost" href="season.html">Get season tickets to our productions</a>
      </div>
    </div>
    <div class="ticket">
      <div class="top-part">
        <div class="lbl">Next on stage · Live at the Capitol</div>
        <img src="{nxt['img']}" alt="{E(nxt['alt'])}">
      </div>
      <div class="bottom-part">
        <div class="d"><small>{nxt['mon'].upper()}</small>{nxt['day']}</div>
        <div class="t"><b>{nxt['title']}</b><span>Friday · 7:30 PM · {nxt['presenter']}</span></div>
        <a class="btn btn-solid" href="show-{nxt['slug']}.html">Get tickets</a>
      </div>
    </div>
  </div>
</section>

<section class="ways" aria-label="Who we are">
  <div class="wrap">
    <div class="way">
      <span class="tag tag-pp">Portal Players Presents</span>
      <h2>Our own plays &amp; musicals</h2>
      <p>Made right here by Alberni Valley volunteers: actors, directors, designers and crew. This is who we are, and it's been happening since 1978.</p>
      <a href="season.html"><b>See this season's productions →</b></a>
    </div>
    <div class="way">
      <span class="tag tag-live">Live at the Capitol</span>
      <h2>Touring shows &amp; rentals</h2>
      <p>Concerts, comedy, tribute acts and community events booked into our theatre. Every ticket helps Portal Players keep this historic 1936 theatre open.</p>
      <a href="rentals.html"><b>Book the theatre →</b></a>
    </div>
  </div>
</section>

{events_block('<div><div class="eyebrow">Coming up</div><h2>What&#39;s On</h2></div>')}

{SEASON_BLOCK}

{NEWS_STRIP}

{INVOLVE_BLOCK}

<section class="block history" id="history">
  <div class="wrap">
    <figure>
      <img src="img/opening-day-1936.png" alt="The Capitol Theatre on opening day, May 16, 1936" width="1260" height="1562" loading="lazy">
      <figcaption>Opening day, May 16, 1936. Photo: A. Joseph Clegg, courtesy of the Alberni Valley Museum.</figcaption>
    </figure>
    <div class="copy">
      <div class="eyebrow">Our story</div>
      <h2>90 years of curtain calls</h2>
      <ol class="timeline">
        <li><b>1936</b>The Capitol opens on May 16 with Bette Davis in <em>Dangerous</em>, 500 seats, air conditioning and a chesterfield in the foyer.</li>
        <li><b>1978</b>Twenty locals meet in the North Island College gym and found Portal Players.</li>
        <li><b>1989</b>Portal Players buy the Capitol. Eight months and $150,000 in grants, donations and volunteer sweat later, it reopens with <em>Something's Afoot</em>.</li>
      </ol>
      <div class="facts">
        <div><strong>230</strong>seats today</div>
        <div><strong>1989</strong>volunteer-owned since</div>
        <div><strong>100%</strong>volunteer-run</div>
      </div>
      <p style="margin:24px 0 0"><a href="history.html"><b>Read the full history →</b></a></p>
    </div>
  </div>
</section>

<section class="block" id="rent">
  <div class="wrap duo">
    <div class="panel">
      <div class="eyebrow">Rentals</div>
      <h2>Put your name on the marquee</h2>
      <p>Concerts, recitals, film nights, memorials and touring shows. Stage, lighting, sound and 230 seats in downtown Port Alberni.</p>
      <a class="btn btn-solid" style="align-self:flex-start;margin-top:8px" href="rentals.html">Request a booking</a>
    </div>
    <div class="panel">
      <div class="shop">
        <img src="img/notebook-cover.jpg" alt="The Capitol Theatre Lined Notebook cover, showing the theatre on opening day in 1936" loading="lazy">
        <div class="t">
          <div class="eyebrow">Fundraiser</div>
          <h2>Capitol Theatre notebooks</h2>
          <p>The 1936 opening-day photo on a 120-page lined journal. $10 from every copy goes to Portal Players.</p>
          <div style="display:flex;flex-wrap:wrap;gap:16px"><a href="https://geni.us/CapitolTheatreLetter1"><b>Large, 8.5 × 11 →</b></a><a href="https://geni.us/CapitolTheatreState1"><b>Small, 5.5 × 8.5 →</b></a></div>
        </div>
      </div>
    </div>
  </div>
</section>'''
    page('index.html', 'The Capitol Theatre · Portal Players', "Port Alberni's home of the performing arts, owned and operated by Portal Players Dramatic Society.", '', body, FILTER_JS + STRIP_JS)

def build_whats_on():
    body = page_head('Calendar', "What's On", 'Every show at The Capitol Theatre, in date order. Red marks our own Portal Players productions; outlined tags are touring acts and rentals.', [(None, "What's On")])
    body += '\n' + events_block(f'<div><div class="eyebrow">2026–27</div><h2>Upcoming shows</h2><p style="margin:8px 0 0;font-size:16px;color:var(--ink-2)">Prefer a calendar? <a href="{GCAL_URL}">Open the theatre&#39;s Google Calendar</a>.</p></div>')
    page('whats-on.html', "What's On · The Capitol Theatre", 'Upcoming shows at The Capitol Theatre in Port Alberni.', 'whats-on.html', body, FILTER_JS)

def build_shows():
    for i, ev in enumerate(EVENTS):
        if 'crop' in ev['thumb']:
            cls = ev['thumb'].replace('crop', '').strip()
            poster = f'<div class="crop-box {cls}"><img src="{ev["img"]}" alt="{E(ev["alt"])}"></div>'
        else:
            poster = f'<img src="{ev["img"]}" alt="{E(ev["alt"])}">'
        pp = ev['kind'] == 'pp'
        tix_href = ev['tix']
        btn_text = 'Buy tickets'
        via = f'<small>Secure checkout via {ev["tixvia"]}</small>' if ev['tixvia'] else ''
        extra_btn = f'<a class="btn btn-ghost" href="{SEASON_URL}">Or get the $79 Season Pass</a>' if pp else ''
        tag_html = tag(ev['kind'])
        by = 'A Portal Players Dramatic Society production' if pp else f'Presented by {ev["presenter"]}'
        age = f'<p><strong>Age:</strong> {ev["age"]}</p>' if ev['age'] else ''
        blurb = ''.join(f'<p>{b if not b.startswith("[") else "<span class=ph>"+b+"</span>"}</p>' for b in ev['blurb'])
        others = [e for e in EVENTS if e is not ev][:3]
        # pick next three by order after this one
        idx = EVENTS.index(ev)
        others = (EVENTS[idx+1:] + EVENTS[:idx])[:3]
        more = '\n'.join(event_row(e) for e in others)
        host_note = '<div class="note">We will do our best to accommodate requests to change performance dates, for Season Pass and single ticket purchases alike. All ticket sales are final, with no refunds.</div>' if pp else '<div class="note">This is a visiting show booked into The Capitol Theatre. Tickets, pricing and refunds are handled by the presenter. Every ticket helps Portal Players keep this historic 1936 theatre open.</div>'
        body = f'''<section class="show-hero">
  <div class="wrap">
    <div class="poster">{poster}</div>
    <div class="details">
      <div class="crumbs"><a href="index.html">Home</a> / <a href="whats-on.html">What's On</a> / {ev['title']}</div>
      {tag_html}
      <h1>{ev['title']}</h1>
      <div class="by">{by}</div>
      <dl class="facts-row">
        <div><dt>Date</dt><dd>{ev['long']}</dd></div>
        <div><dt>Time</dt><dd>{ev['time']}</dd></div>
        <div><dt>Tickets</dt><dd>{ev['price']}</dd></div>
      </dl>
      <div class="ctas">
        <a class="btn btn-amber" href="{tix_href}">{btn_text}</a>{extra_btn}
        {via}
      </div>
    </div>
  </div>
</section>
<section class="block">
  <div class="wrap layout">
    <div class="main prose">
      <h2>About the show</h2>
      {blurb}
      {age}
      {host_note}
    </div>
    <aside class="stack">{VISIT_BOX}</aside>
  </div>
</section>
<section class="block" style="padding-top:0">
  <div class="wrap">
    <div class="head"><div><div class="eyebrow">Also coming up</div><h2>More at the Capitol</h2></div><a href="whats-on.html"><b>All shows →</b></a></div>
    <ol class="events">
{more}
    </ol>
  </div>
</section>'''
        page(f'show-{ev["slug"]}.html', f'{ev["title"]} · The Capitol Theatre', f'{ev["title"]}, {ev["long"]} at The Capitol Theatre, Port Alberni.', 'whats-on.html', body)

def build_season():
    body = page_head('Portal Players Presents', '2026–27 Season Pass', 'Three productions made by Alberni Valley volunteers, on our own stage. One pass, $79.', [(None, 'Season Pass')])
    body += '\n' + SEASON_BLOCK + f'''
<section class="block">
  <div class="wrap layout">
    <div class="main prose">
      <h2>How the Season Pass works</h2>
      <ul>
        <li><strong>$79</strong> gets you into one performance of each of the three productions, a saving of $11 over three $30 single tickets.</li>
        <li>Buy now and <strong>choose your dates and seats later</strong>.</li>
        <li>Passes are sold online through ThunderTix, and at the box office when it opens.</li>
        <li><strong>Coming to Pen Pals?</strong> Buy the whole season before the show, or at the box office when it opens, and you're covered for all three productions.</li>
        <li><strong>Changing dates:</strong> We will do our best to accommodate requests to change performance dates, for Season Pass and single ticket purchases alike. All ticket sales are final, with no refunds.</li>
      </ul>
      <h2>Prefer single tickets?</h2>
      <p>Single tickets are <strong>$30 per person, per production</strong>, and every performance starts at <strong>7:30 PM</strong>. <strong>Single tickets are on sale now.</strong> See <a href="tickets.html">Tickets</a> for all the ways to buy.</p>
      <h2>How our season is chosen</h2>
      <p>Portal Players plans each season about a year ahead. Production proposals are reviewed every February for the following season. Want to direct or pitch a show? <a href="get-involved.html#propose">Find out how</a>.</p>
    </div>
    <aside class="stack">
      <div class="box"><h3>Season Pass</h3><p style="font-family:var(--marquee);font-weight:900;font-size:56px;color:var(--red);line-height:1">$79</p><p>One performance of each production.</p><a class="btn btn-solid" href="{SEASON_URL}">Buy the Season Pass</a></div>
      {VISIT_BOX}
    </aside>
  </div>
</section>'''
    page('season.html', 'Season Pass · Portal Players', 'Portal Players 2026–27 Season Pass: Pen Pals, The Golden Anniversaries and Lips Together, Teeth Apart for $79.', 'season.html', body)

def build_tickets():
    rows = ''
    for ev in EVENTS:
        where = 'Season Pass or single tickets' if ev['kind'] == 'pp' else ev['tixvia'] or 'Presenter'
        href = ev['tix']
        rows += f'<tr><td><b>{ev["title"]}</b><br><span style="font-size:15px;color:var(--ink-2)">{ev["long"]}</span></td><td>{"Portal Players" if ev["kind"]=="pp" else "Visiting show"}</td><td>{where}</td><td><a href="{href}">Buy →</a></td></tr>'
    body = page_head('Box office', 'Tickets', 'Our own productions are sold by Portal Players. Visiting shows are sold by each presenter. Here is where to buy every show.', [(None, 'Tickets')])
    body += f'''
<section class="block">
  <div class="wrap layout">
    <div class="main">
      <div class="cards two">
        <div class="box"><span class="tag tag-pp">Portal Players Presents</span><h3>Season Pass $79, or $30 per person per show</h3><p>The pass covers one performance of each of our three productions; choose dates and seats later. Single tickets are $30 per person, per production. All performances start at 7:30 PM.</p><a class="btn btn-solid" href="{SEASON_URL}">Buy the Season Pass</a></div>
        <div class="box"><span class="tag tag-live">Live at the Capitol</span><h3>Visiting shows</h3><p>Concerts, comedy and touring acts sell tickets through their own ticket sites. Prices and policies are set by the presenter.</p><a class="btn btn-line" href="whats-on.html">Browse visiting shows</a></div>
      </div>
      <h2 style="font-size:34px;margin:52px 0 18px">Every show, where to buy</h2>
      <div class="table-box"><table class="people">
        <thead><tr><th scope="col">Show</th><th scope="col">Type</th><th scope="col">Sold by</th><th scope="col">Buy</th></tr></thead>
        <tbody>{rows}</tbody>
      </table></div>
      <div class="note">At the door: the box office opens one hour before every Portal Players production and takes cash, debit, Mastercard and Visa. Season Passes are also available there. For visiting shows, check the presenter's ticket site for door times.</div>
      <div class="note"><strong>Portal Players productions:</strong> We will do our best to accommodate requests to change performance dates, for Season Pass and single ticket purchases alike. All ticket sales are final, with no refunds.</div>
    </div>
    <aside class="stack">{VISIT_BOX}</aside>
  </div>
</section>'''
    page('tickets.html', 'Tickets · The Capitol Theatre', 'How to buy tickets for every show at The Capitol Theatre.', 'tickets.html', body)

def build_portal_players():
    body = page_head('Who we are', 'Portal Players Dramatic Society', "The Alberni Valley's community theatre company, and the volunteer owner and operator of The Capitol Theatre.", [(None, 'Portal Players')])
    body += f'''
<section class="block">
  <div class="wrap layout">
    <div class="main prose">
      <h2>A volunteer company with its own theatre</h2>
      <p>Portal Players Dramatic Society is a volunteer, membership-driven theatre company in Port Alberni on Vancouver Island. Since 1978 we have been putting Alberni Valley talent on stage, and since 1989 we have owned and run The Capitol Theatre.</p>
      <p>Every actor, director, designer, technician and usher is a volunteer. A board of directors and executive committee, elected by our members, oversees the society and the theatre.</p>
      <h2>What we do</h2>
      <ul>
        <li>Produce an annual season of three or four plays and musicals</li>
        <li>Run improv nights, workshops, rehearsals and auditions</li>
        <li>Host membership and board meetings</li>
        <li>Open the theatre to touring acts, concerts and community events</li>
      </ul>
      <h2>Our vision</h2>
      <p>To build community appreciation for the performing arts, and to be known for progressive, innovative and dynamic entertainment and educational programs.</p>
      <h2>Our mission</h2>
      <p>Portal Players produces plays, runs a civic theatre, and offers educational programs, mentorship and outreach for youth and adults. We work with arts and business partners, advocate for diverse cultural experiences in the Alberni Valley, and operate The Capitol Theatre.</p>
      <p><strong>Ultimately, Portal Players believes in the power of art to bring all people together.</strong></p>
      <h2>Our partners</h2>
      <p>Portal Players Dramatic Society is a member of the Alberni Valley Chamber of Commerce, the Alberni Valley Community Arts Council and Theatre BC. We benefit from the Alberni Valley Community Foundation’s Community Fund Grants, as well as Community Gaming Grants from the Province of BC.</p>
    </div>
    <aside class="stack">
      <div class="box"><h3>Join us</h3><p>Members can act, crew, vote at the AGM and run for the board.</p><a class="btn btn-solid" href="membership.html">Become a member</a></div>
      <div class="box"><h3>Governance</h3><p>Board of directors, committees, constitution and bylaws.</p><a href="board.html"><b>Board &amp; governance →</b></a></div>
      <div class="box"><h3>Our history</h3><p>From a college gym in 1978 to our own 1936 theatre.</p><a href="history.html"><b>Read the story →</b></a></div>
      <div class="box"><h3>Past seasons</h3><p>The plays, musicals, pantos and one-acts we’ve staged since 1988.</p><a href="history.html#past-seasons"><b>See past seasons →</b></a></div>
      <div class="box"><h3>Helen Ford</h3><p>The generous bequest behind the renovation of our theatre and the Helen Ford Lobby.</p><a href="helen-ford.html"><b>Meet Helen Ford →</b></a></div>
    </aside>
  </div>
</section>'''
    page('portal-players.html', 'Portal Players Dramatic Society', "About Portal Players Dramatic Society, the Alberni Valley's community theatre company.", 'portal-players.html', body)

def build_membership():
    body = page_head('Portal Players', 'Membership', 'Members make every show happen. Join to act, crew, volunteer and have your say in how the society is run.', [('portal-players.html', 'Portal Players'), (None, 'Membership')])
    body += f'''
<section class="block">
  <div class="wrap">
    <div class="cards two" style="max-width:820px">
      <div class="box" style="text-align:center"><div class="eyebrow">Individual</div><p style="font-family:var(--marquee);font-weight:900;font-size:64px;color:var(--ink);line-height:1">$10</p><p>per year</p></div>
      <div class="box" style="text-align:center"><div class="eyebrow">Family</div><p style="font-family:var(--marquee);font-weight:900;font-size:64px;color:var(--ink);line-height:1">$20</p><p>per year</p></div>
    </div>
    <p style="margin:22px 0 0"><a class="btn btn-solid" href="{MEMBER_URL}">Join online</a></p>
    <p style="font-size:15px;color:var(--ink-2);margin-top:12px">All memberships expire September 30 each year.</p>
  </div>
</section>
<section class="block" style="padding-top:0">
  <div class="wrap layout">
    <div class="main prose">
      <h2>Why join</h2>
      <ul>
        <li><strong>Get on stage or backstage.</strong> Only PPDS members can take part in productions and activities: actors, production crew, technical operators and all volunteers, including front of house and box office.</li>
        <li><strong>Have your say.</strong> Members in good standing can vote at the Annual General Meeting.</li>
        <li><strong>Lead the society.</strong> Members can run for the board of directors or executive committee.</li>
        <li><strong>Hear it first.</strong> Auditions, workshops and calls for volunteers.</li>
      </ul>
      <div class="note">To vote at the AGM, or to run for the board or executive committee, you must have paid your dues and been a member in good standing for 30 days before the meeting.</div>
      <h2>Life members</h2>
      <p>Portal Players honours these life members for their outstanding service to the society:</p>
      <ul style="columns:2;column-gap:32px"><li>Cindy Solda</li><li>Elliot Drew</li><li>Peter Wienold</li><li>Brent Ronning</li><li>Hannele Talkio</li><li>Diena Tyne</li><li>Teresa Drew</li></ul>
    </div>
    <aside class="stack">
      <div class="box"><h3>Ways to help</h3><p>From acting and directing to costumes, lights, props, box office, poster design and the board of directors: more than thirty ways to help.</p><a href="get-involved.html#volunteer"><b>Volunteer roles →</b></a></div>
      <div class="box"><h3>Members' Facebook group</h3><p>Our private group for Portal Players members: auditions, volunteer calls and backstage news.</p><a href="https://www.facebook.com/groups/10278245586"><b>Join the members' group →</b></a></div>
      <div class="box"><h3>Newsletter only?</h3><p>Email <a href="mailto:capitoltheatre@shaw.ca">capitoltheatre@shaw.ca</a> or sign up at the bottom of this page.</p></div>
    </aside>
  </div>
</section>'''
    page('membership.html', 'Membership · Portal Players', 'Join Portal Players Dramatic Society: $10 individual, $20 family.', 'portal-players.html', body)

def build_get_involved():
    roles = ['Acting', 'Directing', 'Assistant directing', 'Show production', 'Costumes', 'Sewing', 'Wardrobe maintenance', 'Sound', 'Lights', 'Set design', 'Set construction', 'Props', 'Make-up', 'Cast party', 'Concession &amp; refreshments', 'Front of house &amp; ushering', 'Theatre maintenance', 'Clean up', 'Publicity', 'Photography', 'Poster design &amp; distribution', 'Box office sales', 'Corporate sponsorships', 'Play writing', 'Play reading', 'Orchestra', 'Chorus', 'Board of directors', 'Zone festival']
    role_li = ''.join(f'<li>{r}</li>' for r in roles)
    body = page_head('Every seat, light and curtain is volunteer-powered', 'Get Involved', 'Four ways to keep the lights on at the Capitol.', [(None, 'Get Involved')])
    body += f'''
<section class="block">
  <div class="wrap">
    <div class="cards four">
      <a class="box" href="membership.html" style="text-decoration:none;color:inherit"><div class="eyebrow">I</div><h3>Become a member</h3><p>From $10 a year.</p></a>
      <a class="box" href="#volunteer" style="text-decoration:none;color:inherit"><div class="eyebrow">II</div><h3>Volunteer</h3><p>On stage, backstage or front of house.</p></a>
      <a class="box" href="#sponsor" style="text-decoration:none;color:inherit"><div class="eyebrow">III</div><h3>Sponsor Our Season</h3><p>Put your business in the spotlight.</p></a>
      <a class="box" href="#donate" style="text-decoration:none;color:inherit"><div class="eyebrow">IV</div><h3>Donate</h3><p>Support a registered charity.</p></a>
    </div>
  </div>
</section>
<section class="block" style="padding-top:0">
  <div class="wrap layout">
    <div class="main prose">
      <h2 id="volunteer">Volunteer</h2>
      <p>No experience needed. Pick something you love or something you'd like to learn:</p>
      <ul class="roles">{role_li}</ul>
      <p>…and much more!</p>
      <p>Volunteers take part as members of Portal Players. <a href="membership.html">Join from $10 a year</a>, then email <a href="mailto:capitoltheatre@shaw.ca">capitoltheatre@shaw.ca</a> to tell us what interests you.</p>

      <h2 id="propose">Auditions &amp; show proposals</h2>
      <p><strong>Auditions:</strong> subscribe to our email newsletter to get notice of upcoming auditions.</p>
      <p><strong>Proposing a show:</strong> each season is planned about a year ahead. When the season is being developed, our Artistic Direction Committee (ADC) puts out a call for proposals. Subscribe to the email newsletter for updates.</p>

      <h2 id="sponsor">Sponsor Our Season</h2>
      <p>{SP}</p>
      <p><a class="btn btn-solid" href="sponsor.html">See partnership packages</a></p>

      <h2 id="donate">Donate</h2>
      <p>Portal Players Dramatic Society is a federally registered charitable organization and a provincially registered non-profit society. Your gift keeps a 90-year-old building alive and the stage lit for the next generation, and cash donations are tax deductible. Official donation receipts are issued for income tax purposes.</p>
      <p style="font-size:16px"><strong>Charitable registration number:</strong> 89081 5442 RR0001 · <strong>BC Society No.</strong> S-24357</p>
      <ul>
        <li><strong>e-Transfer</strong> to <a href="mailto:capitoltheatre@shaw.ca">capitoltheatre@shaw.ca</a></li>
        <li><strong>Visa or Mastercard</strong>: call 250-723-1195 or drop in at the box office</li>
      </ul>

      <h2 id="notebooks">Buy a notebook</h2>
      <p>Our Capitol Theatre lined notebooks feature the 1936 opening-day photo. $10 from every copy goes to Portal Players. Produced in partnership with PWA Publishing.</p>
      <p><a href="https://geni.us/CapitolTheatreLetter1"><b>Large, 8.5 × 11 →</b></a> &nbsp; <a href="https://geni.us/CapitolTheatreState1"><b>Small, 5.5 × 8.5 →</b></a></p>
    </div>
    <aside class="stack">
      <img src="img/notebook-cover.jpg" alt="The Capitol Theatre Lined Notebook cover" style="max-width:260px;box-shadow:0 14px 28px rgba(60,40,20,.25)" loading="lazy">
      {VISIT_BOX}
    </aside>
  </div>
</section>'''
    page('get-involved.html', 'Get Involved · Portal Players', 'Volunteer, become a member, sponsor our season or donate to Portal Players.', 'get-involved.html', body)

def build_rentals():
    body = page_head('Live at the Capitol', 'Rent the Theatre', 'Concerts, recitals, film nights, memorials, conferences and touring shows. Put your name on the marquee in downtown Port Alberni.', [(None, 'Rentals')])
    body += f'''
<section class="block">
  <div class="wrap layout">
    <div class="main prose">
      <h2>The space</h2>
      <div class="cards" style="margin-bottom:28px">
        <div class="box"><p style="font-family:var(--marquee);font-weight:900;font-size:48px;color:var(--red);line-height:1">230</p><p>seats</p></div>
        <div class="box"><p style="font-family:var(--marquee);font-weight:900;font-size:48px;color:var(--red);line-height:1">1936</p><p>historic movie palace</p></div>
        <div class="box"><p style="font-family:var(--marquee);font-weight:900;font-size:48px;color:var(--red);line-height:1">Ramp</p><p>access to the main lobby</p></div>
      </div>
      <ul>
        <li>Stage with lighting and sound</li>
        <li>The Helen Ford Lobby for front of house and receptions</li>
        <li>Dressing and makeup rooms behind the stage</li>
        <li>Downtown location at 4th Avenue and Argyle Street, with street parking nearby</li>
      </ul>
      <h2>Rates &amp; what's included</h2>
      <p>For rental rates, availability and technical details, email <a href="mailto:capitoltheatre@shaw.ca?subject=Rental%20enquiry">capitoltheatre@shaw.ca</a> or use the booking enquiry form below.</p>
      <div class="note">Every rental helps Portal Players keep this historic 1936 theatre open. Your show will be listed on our What's On page as "Live at the Capitol."</div>
      <h2 id="enquire">Booking enquiry</h2>
      <form class="form" action="mailto:capitoltheatre@shaw.ca" method="post" enctype="text/plain">
        <label>Your name<input name="name" autocomplete="name"></label>
        <label>Organisation<input name="organisation" autocomplete="organization"></label>
        <label>Email<input type="email" name="email" autocomplete="email"></label>
        <label>Phone<input type="tel" name="phone" autocomplete="tel"></label>
        <label>Type of event<select name="type"><option>Concert</option><option>Theatre or dance</option><option>Recital</option><option>Film screening</option><option>Memorial or celebration</option><option>Meeting or conference</option><option>Other</option></select></label>
        <label>Preferred date(s)<input name="dates"></label>
        <label class="full">Tell us about your event<textarea name="details"></textarea></label>
        <div class="full"><button class="btn btn-solid" type="submit" style="border:0;cursor:pointer">Send enquiry</button></div>
      </form>
    </div>
    <aside class="stack">
      <div class="box dark"><h3 style="color:#F3EEE4">Talk to us</h3><p>Call <a href="tel:2507231195">250-723-1195</a> or email <a href="mailto:capitoltheatre@shaw.ca">capitoltheatre@shaw.ca</a>.</p></div>
      <img src="img/opening-day-1936.png" alt="The Capitol Theatre building" loading="lazy" style="filter:sepia(.3)">
    </aside>
  </div>
</section>'''
    page('rentals.html', 'Rent the Theatre · The Capitol Theatre', 'Rent The Capitol Theatre in Port Alberni: 230 seats, stage, lighting and sound.', 'rentals.html', body)

def build_history():
    body = page_head('Our story', '90 Years of Curtain Calls', 'From a silent-movie house to the Alberni Valley\'s home of the performing arts.', [('portal-players.html', 'Portal Players'), (None, 'Our history')])
    body += '''
<section class="block">
  <div class="wrap layout">
    <div class="main prose">
      <h2>The Port Theatre, 1914</h2>
      <p>Before the Capitol, there was the Port Theatre on First Avenue, across from Alberni Hardware. Jack Warren opened it in 1914. It seated 200, showed films every Wednesday and Saturday night, and an Edison cylinder gramophone supplied the music for the silent pictures.</p>
      <h2>The Capitol opens, 1936</h2>
      <p>Talking pictures arrived in 1929. In the hard years of the mid-1930s, Jack Warren saw the need for a larger, modern theatre and bought the corner of Fourth Avenue and Argyle Street in 1934. He died in December 1935 and never saw it open. His wife Louise and son Harold took over.</p>
      <p>The Capitol Theatre opened on May 16, 1936, with Bette Davis in <em>Dangerous</em>. A 1937 newspaper called it a "community asset," with 500 seats, air conditioning, a modern sound system and a large chesterfield in the foyer. It ran as a cinema until the late 1970s.</p>
      <h2>Portal Players is born, 1978</h2>
      <p>In the fall of 1978, about twenty Port Alberni residents met in the North Island College gymnasium to talk about forming a drama group. Among them were Allan Markin, Gordon Scoffield, John Andrews, Margita Hartman, David Lord and Pam Aspinall. The college gym became their first stage, with risers built for effect and the staff room serving as the green room. Admission was free at first.</p>
      <p>Through the 1980s the company staged production after production, including <em>Funeral Tea</em>, <em>Street of Dreams</em>, <em>A Family Christmas</em> (1984), a sold-out <em>The Odd Couple</em> (1985), <em>Sing A Song of Sixpence</em> (1986) and <em>Cheating Cheaters</em> (1988). Portal Players competed in the North Island Zone Theatre BC festivals, winning praise for "thoroughly professional backstage skills" and individual awards.</p>
      <h2>Buying the Capitol, 1989</h2>
      <p>Looking for a bigger home, the members set their sights on the old Capitol. In 1989, against the better judgment of some, they bought it, and never looked back. The roof was repaired, dressing and makeup rooms were built, the washrooms rebuilt, and lighting and sound installed. It took more than $150,000 in grants and donations, eight months and countless volunteer hours. Project manager Maurice Farn called it "the impossible dream."</p>
      <p>The new home opened on September 27, 1989, with <em>Something's Afoot</em>, followed that Christmas by <em>The Red Shoes</em>, the first show to use the new curtains.</p>
      <h2>The 1990s and beyond</h2>
      <p>Highlights include <em>Harvey</em>, which drew a record 750 patrons despite a blizzard on opening night, <em>Mark of Cain</em> (1994), <em>Beauty and the Beast</em>, and <em>Opening Night</em>, winner of three awards at the 1993 North Island Zone Drama Festival.</p>
      <p>A later bequest from Helen Ford funded a major renovation of the front of house, now the <a href="helen-ford.html">Helen Ford Lobby</a>.</p>
      <div class="note">Adapted from <em>Portal Players Dramatic Society and the Capitol Theatre: A Brief History</em>, a 20th-anniversary project (1999). With thanks to the Alberni Valley Museum &amp; Photographic Archives, Joan Frohn-Nielsen, Pam Aspinall, Cindy Solda and Harold Warren.</div>
    </div>
    <aside class="stack">
      <figure style="margin:0"><img src="img/opening-day-1936.png" alt="The Capitol Theatre on opening day, May 16, 1936" loading="lazy" style="filter:sepia(.25)"><figcaption style="font-size:14px;color:var(--ink-2);margin-top:8px;font-style:italic;font-family:var(--serif)">Opening day, May 16, 1936. Photo: A. Joseph Clegg, courtesy of the Alberni Valley Museum.</figcaption></figure>
      <div class="box"><h3>At a glance</h3><dl><dt>1914</dt><dd>Port Theatre opens</dd><dt>1936</dt><dd>The Capitol opens</dd><dt>1978</dt><dd>Portal Players founded</dd><dt>1989</dt><dd>PPDS buys the Capitol</dd><dt>Today</dt><dd>230 seats, volunteer-run</dd></dl></div>
      <div class="box dark"><h3 style="color:#F3EEE4">Past seasons</h3><p>Every production we know of, from 1988 to today.</p><a href="#past-seasons"><b>See the list →</b></a></div>
      <div class="box"><h3>Helen Ford</h3><p>The generous bequest behind the renovation of our theatre and the Helen Ford Lobby.</p><a href="helen-ford.html"><b>Meet Helen Ford →</b></a></div>
    </aside>
  </div>
</section>'''
    body += seasons.render()
    page('history.html', 'Our History · The Capitol Theatre', 'The history of The Capitol Theatre and Portal Players Dramatic Society.', 'portal-players.html', body)

def build_helen():
    body = page_head('The Helen Ford Lobby', 'Helen Ford', '', [('history.html', 'Our history'), (None, 'Helen Ford')])
    body += '''
<section class="block">
  <div class="wrap">
    <div class="prose" style="max-width:820px">
      <figure style="float:left;margin:6px 32px 20px 0;width:175px">
        <img src="img/helen-ford.jpg" alt="Helen and Armour Ford at their home at Sproat Lake." width="175" height="296" style="box-shadow:0 12px 26px rgba(60,40,20,.25)">
        <figcaption style="font-family:var(--serif);font-style:italic;font-size:14px;color:var(--ink-2);margin-top:10px">Helen and Armour Ford at their home at Sproat Lake.</figcaption>
      </figure>
      <p>Helen Ford’s generosity included a bequest to enhance the local theatre community with a performing arts space. Ultimately, this bequest was used to completely renovate The Capitol Theatre – and especially the front of house, lobby, concession area, costume room, public washrooms, members lounge &amp; furnishings, and tech room. It is in her honour that we have named our front of house the Helen Ford Lobby.</p>
      <p>Bequest funds also helped to leverage additional grants from Cultural Spaces Canada, The Province of BC, and the Vancouver Foundation to aid in this renovation work. Individual donations have also contributed to the completion work of The Capitol Theatre. Additional renovations included a makeover of the green room, installation of a new roof, enhancement of the lighting and sound systems, creation of a proper office space &amp; equipment, a total refit of the stage curtains &amp; hardware, implementation of an electronic box office with reserved seating, and the wondrous front exterior which features a new entrance canopy and marquee sign.</p>
      <p>Portal Players Dramatic Society sincerely thanks Helen Ford and the estate for their generosity in allowing this work to take place. The Capitol Theatre is now, truly, “Home of the Performing Arts” in Port Alberni.</p>
      <hr style="clear:both;border:0;border-top:1px solid var(--rule);margin:36px 0">
      <h2>About Helen Ford</h2>
      <p>Helen Ford first saw the Alberni Valley in 1926 when her father purchased the Sproat Lake Logging Co. and renamed it Sproat Lake Sawmills. She loved the lake and determined to spend as much time as possible there. This was easy because her parents were living at Kleecoot. She built herself a small cabin across Stirling Arm and gradually fitted into the community. World War II found her enlisted in the Canadian Women’s Army Corp as an officer. In 1946 she was awarded an M.B.E. for her Service.</p>
      <p>Following her marriage to Armour Ford in 1953 they came to Sproat Lake to take up permanent residence. Armour was called to the bar in British Columbia and practiced law locally until his retirement. However, it was as a community-minded couple that the Fords made a very special contribution to their adopted home. Helen was active in the Women’s Auxiliary to the West Coast General Hospital, a founding member of the Community Arts Council, an elected member of the Board for School District #70, and a member of the Mt. Klitsa Garden Club. Armour’s name appears as a supporter of the Naval Cadets and for many years was the treasurer of the Alberni District Historical Society.</p>
      <p>Prior to 1965, Helen, Ketha Adams, and a few other like-minded citizens had serious concerns for the documentation of the History of the Alberni Valley. They began collecting artifacts and archival material, and persuaded the Mayors of the twin citys, Les Hammer and Fred Bishop to support their cause. The A.D.H.S. came into being in 1965. What was needed next was a museum to hold the growing collection. That became a reality in 1972, to be followed in 1983 by an expansion. This expansion allowed the Archival Collection to be moved from a totally inadequate workshop in the old Army Camp Fire Hall to a safe venue in the new space.</p>
      <p>Helen’s interest in the indigenous community was genuine and out of it grew many personal friendships. Her support of cultural events and local organizations was on going and frequently very low key. In 1983 Helen and Armour Ford were named “Citizens of the Year”, a well-deserved acknowledgement of their presence among us.</p>
      <p>From the little cabin Helen built to use on her frequent visits to Sproat Lake, to the larger home she and Armour built on the same property across from their residence on Stirling Arm Drive, Helen made good her promise to herself “live at the Lake”. In due course, this 130 acres of land, complete with a waterfall, was given to the people of British Columbia as a day-use Park. Fossli, a waterfall in a meadow, now became a small paradise for those who hike into it or arrive by boat.</p>
      <p>Helen’s health began to fail following the death of Armour, and she herself passed away in May of 1997 at age 91. But her kindness was not yet over. In her will, she bequeathed to the A.D.H.S. a sum of money, documents, books, and artifacts which have spread out to continue to bless us all. Helen Lake up on Porter Ridge is named in her memory.</p>
      <p>Thank you Helen.</p>
      <p><em>Courtesy Alberni District Historical Society</em></p>
    </div>
  </div>
</section>'''
    page('helen-ford.html', 'Helen Ford · The Capitol Theatre', 'Helen Ford, whose bequest renovated The Capitol Theatre; the front of house is named the Helen Ford Lobby in her honour.', 'portal-players.html', body)

def build_board():
    board = [('President', 'Liane Fitzpatrick'), ('Vice-President', 'Diena Tyne'), ('Treasurer', 'Meloney Edghill'), ('Secretary', 'Brent Ronning'),
             ('Directors at Large', 'Ojas Cats, Branden Chase, Nicole Foster, Drew Waveryn, Peter Wienold')]
    comm = [('Representative to Theatre BC', 'Nicole Foster'), ('Artistic Direction Committee Chair', 'Peter Wienold'), ('Finance Committee Chair', 'Meloney Edghill'), ('Play Reading Committee', 'Nicole Foster, Brent Ronning')]
    tr = lambda rows: ''.join(f'<tr><th scope="row" style="font-family:var(--sans);font-size:16px;letter-spacing:0;text-transform:none;color:var(--ink)">{a}</th><td>{b}</td></tr>' for a, b in rows)
    body = page_head('Portal Players', 'Board &amp; Governance', 'Portal Players is run by a volunteer board elected by our members each September.', [('portal-players.html', 'Portal Players'), (None, 'Board &amp; governance')])
    body += f'''
<section class="block">
  <div class="wrap layout">
    <div class="main prose">
      <h2>2026–27 Board of Directors</h2>
      <div class="table-box"><table class="people"><tbody>{tr(board)}</tbody></table></div>
      <h2>Committees &amp; representatives</h2>
      <div class="table-box"><table class="people"><tbody>{tr(comm)}</tbody></table></div>
      <h2>Annual General Meeting</h2>
      <p>The next AGM will be held in <strong>September 2027</strong> at The Capitol Theatre. The date will be announced to members. To vote or stand for election, you must be a <a href="membership.html">member</a> in good standing for 30 days before the meeting.</p>
      <h2>Constitution &amp; bylaws</h2>
      <ul class="docs">
        <li><div><b>PPDS Constitution</b><span>For transition to the new Societies Act, September 2018</span></div><a href="https://wp.me/a9b4wN-t2">View PDF →</a></li>
        <li><div><b>PPDS Bylaws</b><span>Amended by special resolution, AGM, September 30, 2020</span></div><a href="http://atthecapitol.org/wp-content/uploads/2020/10/2020.09.30-PPDS-Bylaw-Revisions.pdf">View PDF →</a></li>
      </ul>
      <h2>Board meeting minutes</h2>
      <p>Board meeting minutes are available to members on request. Email <a href="mailto:capitoltheatre@shaw.ca?subject=Board%20minutes%20request">capitoltheatre@shaw.ca</a>.</p>
    </div>
    <aside class="stack">
      <div class="box"><h3>Contact the board</h3><p>Email <a href="mailto:capitoltheatre@shaw.ca">capitoltheatre@shaw.ca</a> or call 250-723-1195.</p></div>
      <div class="box"><h3>Vision &amp; mission</h3><p>Why Portal Players exists and what we do.</p><a href="portal-players.html"><b>Who we are →</b></a></div>
    </aside>
  </div>
</section>'''
    page('board.html', 'Board & Governance · Portal Players', 'Portal Players Dramatic Society board of directors, committees, constitution and bylaws.', 'portal-players.html', body)

def build_visit():
    body = page_head('Plan your visit', 'Visit &amp; Contact', 'Everything you need for a night at the Capitol.', [(None, 'Visit &amp; contact')])
    body += f'''
<section class="map-band" aria-label="Map">
  <iframe title="Map showing The Capitol Theatre, 4904 Argyle Street, Port Alberni" src="https://www.google.com/maps?q=Capitol+Theatre,+4904+Argyle+Street,+Port+Alberni,+BC&amp;z=16&amp;output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade" tabindex="-1" aria-hidden="true"></iframe>
  <a class="map-link" href="{MAP_URL}" target="_blank" rel="noopener" aria-label="Open The Capitol Theatre, 4904 Argyle Street, in Google Maps"><span>4904 Argyle Street, Port Alberni · Open in Google Maps →</span></a>
</section>
<section class="block">
  <div class="wrap">
    <div class="cards">
      <div class="box"><h3>Find us</h3><p>4904 Argyle Street<br>Port Alberni, BC V9Y 1V7<br>At the corner of 4th Avenue and Argyle Street.</p><a href="{MAP_URL}"><b>Open in Google Maps →</b></a></div>
      <div class="box"><h3>Box office</h3><p>Opens one hour before every Portal Players production.</p><p>We accept cash, debit, Mastercard and Visa.</p></div>
      <div class="box"><h3>Parking</h3><p>Street parking is available around the theatre on Argyle Street, 4th Avenue and nearby streets.</p></div>
      <div class="box"><h3>Accessibility</h3><p>A ramp leads to the main lobby doors on Argyle Street. Need a hand on arrival? Call 250-723-1195 ahead of the show.</p><p>Accessible seating and an accessible washroom are available.</p></div>
      <div class="box"><h3>Visiting shows</h3><p>For touring acts and rentals, tickets and door times are handled by each presenter. Check the show page for details.</p></div>
      <div class="box"><h3>During the show</h3><p>No photos or video during performances, please.</p><p>Late seating is discouraged, but may be accommodated on occasion.</p></div>
    </div>
  </div>
</section>
<section class="block" id="contact" style="padding-top:0">
  <div class="wrap layout">
    <div class="main prose">
      <h2>Contact us</h2>
      <p>Call <a href="tel:2507231195">250-723-1195</a> or email <a href="mailto:capitoltheatre@shaw.ca">capitoltheatre@shaw.ca</a>. For rentals, use our <a href="rentals.html#enquire">booking enquiry form</a>.</p>
      <form class="form" action="mailto:capitoltheatre@shaw.ca" method="post" enctype="text/plain">
        <label>Your name<input name="name" autocomplete="name"></label>
        <label>Email<input type="email" name="email" autocomplete="email"></label>
        <label class="full">Subject<select name="subject"><option>General question</option><option>Tickets</option><option>Membership</option><option>Volunteering</option><option>Sponsorship</option><option>Rentals</option></select></label>
        <label class="full">Message<textarea name="message"></textarea></label>
        <div class="full"><button class="btn btn-solid" type="submit" style="border:0;cursor:pointer">Send message</button></div>
      </form>
    </div>
    <aside class="stack">
      <div class="box"><h3>Follow us</h3><p>Show news, photos and announcements on our public Facebook page.</p><a href="https://www.facebook.com/CapitolTheatrePortAlberni"><b>The Capitol Theatre on Facebook →</b></a><a href="https://www.instagram.com/at.the.capitol.theatre/"><b>@at.the.capitol.theatre on Instagram →</b></a><p>Watch clips and videos from our productions.</p><a href="https://www.youtube.com/@PortalPlayers"><b>Portal Players on YouTube →</b></a></div>
      <div class="box dark"><h3 style="color:#F3EEE4">Mailing address</h3><p>The Capitol Theatre<br>Portal Players Dramatic Society<br>4904 Argyle Street<br>Port Alberni, BC V9Y 1V7</p></div>
    </aside>
  </div>
</section>'''
    page('visit.html', 'Visit & Contact · The Capitol Theatre', 'Address, box office, parking, accessibility and contact details for The Capitol Theatre.', 'visit.html', body)

PACKAGES = [
    ('Patron', 'Individual', '$120', ['One Season Ticket', 'Patron Thank You listing', 'Membership in Portal Players']),
    ('Stage Crew', '', '$220', ['Two Season Tickets', 'Patron Thank You listing', 'Family Membership in Portal Players']),
    ('Tech Crew', '', '$550', ['Four Season Tickets', 'Patron Thank You listing', 'Logo on our Lobby Display Screen', 'Logo on our Show Posters', 'Small Ad in Show Programs']),
    ('Stage Manager', '', '$1,000', ['Four Season Tickets', 'Patron Thank You listing', 'Logo on our Lobby Display Screen', 'Logo on our Show Posters', 'Business named in pre-show announcement', 'Medium Ad in Show Programs']),
    ('Director', '', '$2,500', ['Six Season Tickets', 'Patron Thank You listing', 'Logo on our Lobby Display Screen', 'Lobby Display Space to promote your business (info table available on request)', 'Large Logo on our Show Posters', 'Business named in pre-show announcement', 'Business recognition in our social posts', 'Large Ad in Show Programs']),
    ('Producer', '', '$3,000+', ['Eight Season Tickets', 'Patron Thank You listing', 'Digital Advertisement on our Lobby Display Screen', 'Lobby Display Space to promote your business (info table available on request)', 'Large Logo on our Show Posters', 'Business named in pre-show announcement', 'Business recognition in our social posts', 'Largest Ad in Show Programs']),
]

def build_sponsor():
    cards=''
    for name, sub, price, perks in PACKAGES:
        top = name in ('Director', 'Producer')
        lis=''.join(f'<li>{x}</li>' for x in perks)
        subt = f' <span style="font-family:var(--sans);font-size:15px;font-weight:400;color:var(--ink-2)">({sub})</span>' if sub else ''
        style = ' style="border:2px solid var(--red)"' if top else ''
        cards += f'''<div class="box"{style}><div class="eyebrow">{'Top tier' if name=='Producer' else 'Partnership package'}</div><h3 style="font-size:28px">{name}{subt}</h3><p style="font-family:var(--marquee);font-weight:900;font-size:52px;color:var(--red);line-height:1">{price}</p><ul style="margin:0;padding-left:20px;color:var(--ink-2);font-size:16px;display:flex;flex-direction:column;gap:4px">{lis}</ul></div>'''
    opts=''.join(f'<option>{n} ({p})</option>' for n,_,p,_ in PACKAGES)
    body = page_head('Sponsor Our Season', 'Partnership Packages', 'Our audiences and members are your customers. Partner with Portal Players and turn our promotion into your promotion.', [('get-involved.html', 'Get Involved'), (None, 'Sponsor our season')])
    body += f'''
<section class="block">
  <div class="wrap">
    <div class="cards four" style="margin-bottom:56px">
      <div><h3 style="font-size:22px">Your customers are here</h3><p style="color:var(--ink-2);font-size:16px;margin:8px 0 0">The Capitol hosts events all season, and our promotion is seen throughout the Alberni Valley.</p></div>
      <div><h3 style="font-size:22px">Support the arts</h3><p style="color:var(--ink-2);font-size:16px;margin:8px 0 0">Keep the performing arts alive here, and show you value a vibrant, well-rounded community.</p></div>
      <div><h3 style="font-size:22px">Community involvement</h3><p style="color:var(--ink-2);font-size:16px;margin:8px 0 0">People notice and respect businesses that give back to the community that supports them.</p></div>
      <div><h3 style="font-size:22px">Great value</h3><p style="color:var(--ink-2);font-size:16px;margin:8px 0 0">A year-long partnership costs less than a single ad in most other media.</p></div>
    </div>
    <div class="head"><div><div class="eyebrow">2026–27 season</div><h2>Choose your package</h2></div></div>
    <div class="cards">{cards}</div>
    <p style="font-size:15px;color:var(--ink-2);margin-top:18px">Every package includes season tickets to our three Portal Players productions.</p>
  </div>
</section>
<section class="block" style="padding-top:0" id="join">
  <div class="wrap layout">
    <div class="main prose">
      <h2>Become a partner</h2>
      <p>Pay by <strong>e-Transfer</strong> to <a href="mailto:capitoltheatre@shaw.ca">capitoltheatre@shaw.ca</a>, or by <strong>Visa or Mastercard</strong> (drop in to process your payment). Additional donations are welcome with any package.</p>
      <p>Or send us your details and we'll be in touch:</p>
      <form class="form" action="mailto:capitoltheatre@shaw.ca?subject=Sponsorships" method="post" enctype="text/plain">
        <label>Business<input name="business" autocomplete="organization"></label>
        <label>Contact name<input name="contact" autocomplete="name"></label>
        <label>Email<input type="email" name="email" autocomplete="email"></label>
        <label>Phone<input type="tel" name="phone" autocomplete="tel"></label>
        <label>Website<input name="website" autocomplete="url"></label>
        <label>Package<select name="package">{opts}<option>Additional donation</option></select></label>
        <label class="full">Name to print in our Thank You listing<input name="thankyou"></label>
        <div class="full"><button class="btn btn-solid" type="submit" style="border:0;cursor:pointer">Send partnership request</button></div>
      </form>
    </div>
    <aside class="stack">
      <div class="box dark"><h3 style="color:#F3EEE4">Questions?</h3><p>Email <a href="mailto:capitoltheatre@shaw.ca?subject=Sponsorships">capitoltheatre@shaw.ca</a> with the subject line <strong style="color:#F3EEE4">Sponsorships</strong>, attention Diena.</p><p>Or call 250-723-1195.</p></div>
      <div class="box"><h3>A registered charity</h3><p>Portal Players Dramatic Society is a federally registered charitable organization and a provincially registered non-profit society. Cash donations are tax deductible. Charitable registration no. 89081 5442 RR0001.</p></div>
      <div class="box"><h3>Thank you, marquee sponsors</h3><div class="sp-row light"><a class="sp-logo flush" href="https://www.thegraphicsfactory.com" target="_blank" rel="noopener"><img src="img/sponsor-graphics-factory.png" alt="Graphics Factory Printing &amp; Signs" loading="lazy"></a><span class="sp-logo"><img src="img/sponsor-coop.png" alt="Alberni District Co-op" loading="lazy"></span><a class="sp-logo" href="https://dbasilencing.ca" target="_blank" rel="noopener"><img src="img/sponsor-dba.png" alt="DBA Metal Art" loading="lazy"></a><span class="sp-logo"><img src="img/sponsor-tpa.png" alt="Tim Pley &amp; Associates" loading="lazy"></span></div><p style="font-size:14px">DBA Metal Art · The Graphics Factory · Alberni District Co-op · Tim Pley &amp; Associates</p></div>
    </aside>
  </div>
</section>'''
    page('sponsor.html', 'Sponsor Our Season · Portal Players', 'Portal Players partnership packages from $120 to $3,000+: season tickets, logos, programme ads and lobby display space.', 'get-involved.html', body)

# ------------------------------------------------------------------ live-only files
# Old WordPress addresses (atthecapitol.org/?page_id=… and ?p=…) and where they now live.
OLD_PAGES = {'84': 'tickets.html', '26': 'whats-on.html', '2': 'portal-players.html', '66': 'visit.html',
             '51': 'membership.html', '90': 'board.html', '1163': 'portal-players.html', '92': 'board.html',
             '69': 'history.html', '71': 'helen-ford.html'}
OLD_POSTS = {'2676': 'season.html', '2673': 'show-killer-bands-from-outer-space.html',
             '2668': 'show-comic-strippers.html', '2640': 'show-improv-comedy-rumble.html',
             '2650': 'show-dreams-arrival.html', '2066': 'get-involved.html', '2168': 'membership.html'}

def build_404():
    body = f'''<section class="block">
  <div class="wrap prose" style="max-width:760px">
    <div class="eyebrow">Page not found</div>
    <h1 style="font-size:clamp(36px,5vw,56px);margin:10px 0 16px">This scene isn&#39;t in the script</h1>
    <p>The page you were looking for has moved or no longer exists. Our website has a new look, so some old links no longer work.</p>
    <p><a class="btn btn-solid" href="whats-on.html">See what&#39;s on</a> &nbsp; <a href="index.html"><b>Go to the home page →</b></a></p>
  </div>
</section>'''
    page('404.html', 'Page not found · The Capitol Theatre', 'Page not found.', '', body, base=True)

def build_live_extras():
    build_404()
    pages = sorted(f for f in os.listdir(OUT) if f.endswith('.html') and f != '404.html')
    pages.sort(key=lambda f: (f != 'index.html', f))
    urls = ''.join(f'  <url><loc>{SITE_URL}{"" if f == "index.html" else f[:-5]}</loc></url>\n' for f in pages)
    open(os.path.join(OUT, 'sitemap.xml'), 'w').write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + '</urlset>\n')
    open(os.path.join(OUT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}sitemap.xml\n')
    b = SITE_BASE
    rules = []
    for pid, dest in OLD_PAGES.items():
        rules.append(f'RewriteCond %{{QUERY_STRING}} (^|&)page_id={pid}(&|$)\nRewriteRule ^(index\\.php)?$ {b}{dest[:-5]}? [R=301,L]')
    for pid, dest in OLD_POSTS.items():
        rules.append(f'RewriteCond %{{QUERY_STRING}} (^|&)p={pid}(&|$)\nRewriteRule ^(index\\.php)?$ {b}{dest[:-5]}? [R=301,L]')
    rules.append(f'# Any other old post or page\nRewriteCond %{{QUERY_STRING}} (^|&)p=[0-9]+(&|$)\nRewriteRule ^(index\\.php)?$ {b}whats-on? [R=301,L]')
    rules.append(f'RewriteCond %{{QUERY_STRING}} (^|&)(page_id|author|cat|m)=\nRewriteRule ^(index\\.php)?$ {b}? [R=301,L]')
    rules.append(f'# Old WordPress folders and feeds\nRewriteRule ^(wp-admin|wp-login\\.php|wp-content|wp-includes|feed|comments)(/.*)?$ {b} [R=301,L]')
    ht = f'''# The Capitol Theatre: atthecapitol.org (generated by src/build.py; edit there, not here)
Options -Indexes
DirectoryIndex index.html
ErrorDocument 404 {b}404.html

<IfModule mod_rewrite.c>
RewriteEngine On
RewriteBase {b}

# Always use https, and drop "www." (keeps whichever address was used, e.g. new.atthecapitol.org for previews)
RewriteCond %{{HTTP_HOST}} ^www\\.(.+)$ [NC]
RewriteRule ^(.*)$ https://%1{b}$1 [R=301,L]
RewriteCond %{{HTTPS}} !=on
RewriteRule ^(.*)$ https://%{{HTTP_HOST}}{b}$1 [R=301,L]

# Old WordPress links -> new pages
''' + '\n\n'.join(rules) + f'''

# Clean addresses: /visit.html -> /visit (and /index.html -> /)
RewriteCond %{{THE_REQUEST}} \\s/+(.*?/)?index\\.html[\\s?] [NC]
RewriteRule ^ {b}%1 [R=301,L]
RewriteCond %{{THE_REQUEST}} \\s/+([^?\\s]+?)\\.html[\\s?] [NC]
RewriteRule ^ /%1 [R=301,L]

# Drop a trailing slash on page addresses: /visit/ -> /visit
RewriteCond %{{REQUEST_FILENAME}} !-d
RewriteRule ^(.+)/$ {b}$1 [R=301,L]

# Serve /visit from visit.html
RewriteCond %{{REQUEST_FILENAME}} !-d
RewriteCond %{{REQUEST_FILENAME}}.html -f
RewriteRule ^(.+?)/?$ $1.html [L]
</IfModule>

<IfModule mod_expires.c>
ExpiresActive On
ExpiresByType text/html "access plus 10 minutes"
ExpiresByType text/css "access plus 1 year"
ExpiresByType image/png "access plus 1 month"
ExpiresByType image/jpeg "access plus 1 month"
ExpiresByType image/webp "access plus 1 month"
</IfModule>
'''
    open(os.path.join(OUT, '.htaccess'), 'w').write(ht)

def main():
    css = open(os.path.join(HERE, 'base.css')).read() + EXTRA_CSS + seasons.CSS
    open(os.path.join(OUT, 'site.css'), 'w').write(css)
    global CSS_VER
    CSS_VER = hashlib.sha1(css.encode()).hexdigest()[:8]
    build_home(); build_whats_on(); build_shows(); build_season(); build_tickets()
    build_portal_players(); build_membership(); build_get_involved(); build_rentals()
    build_history(); build_helen(); build_board(); build_visit(); build_sponsor()
    if not NOINDEX:
        build_live_extras()
    print(sorted(f for f in os.listdir(OUT) if f.endswith('.html')))

main()
