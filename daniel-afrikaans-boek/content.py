# -*- coding: utf-8 -*-
"""Inhoud van 'Daniel se Afrikaans Avontuur' (Graad 3 werkboek).

Elke hoofstuk (vlak) het:
  title, key (taalonderwerp), story (paragrawe), vocab, questions, tf,
  explain, exA, exB, spell, writing
Items in questions: (vraag, antwoord, open?)
Items in exA/exB:  (teks, antwoord)  met mode: word | blank | line | none
"""

CHAPTERS = [
    # ------------------------------------------------------------------ 1
    dict(
        title="Die Bus in die Lug",
        key="Naamwoorde",
        story=[
            "Daniel sit op die groot, blou bus. Die bus vlieg hoog bo die eiland. Onder hom sien hy berge, riviere en 'n kasteel.",
            "“Vandag gaan ons wen!” sê Daniel vir sy maat, Lisa. Lisa lag. “Eers moet ons 'n goeie plek kry om te land,” sê sy.",
            "Daniel kyk na die kaart. Hy sien 'n dorp met baie huise en 'n blink meer. “Daar!” roep hy. Hulle spring uit die bus en sweef na die grond. Die wind waai in hul gesigte. Dis die beste deel van die dag!",
        ],
        vocab=[("eiland", "land met water rondom"), ("kaart", "dit wys vir jou waar dinge is"),
               ("maat", "'n vriend of spanmaat"), ("sweef", "stadig deur die lug beweeg")],
        questions=[
            ("Waarop sit Daniel aan die begin van die storie?", "Op die groot, blou bus.", False),
            ("Noem twee dinge wat Daniel onder hom sien.", "Enige twee: berge, riviere, 'n kasteel.", False),
            ("Wie is Daniel se maat?", "Lisa.", False),
            ("Waar wil Daniel land?", "By die dorp langs die meer.", False),
            ("Hoekom dink jy sê Daniel: “Dis die beste deel van die dag”?", "Open vraag – enige goeie antwoord.", True),
        ],
        tf=[("Die bus ry op die grond.", False), ("Daniel gebruik 'n kaart.", True), ("Lisa is hartseer.", False)],
        explain="'n <b>Naamwoord</b> is die naam van 'n <b>persoon</b>, 'n <b>plek</b> of 'n <b>ding</b>.<br/>"
                "Voorbeelde: <b>Daniel</b> (persoon), <b>eiland</b> (plek), <b>kaart</b> (ding).",
        exA=dict(title="Skryf die naamwoord in elke sin neer.", mode="word", items=[
            ("Die bus is blou.", "bus"), ("Lisa lag hard.", "Lisa"), ("Die berg is hoog.", "berg"),
            ("Ek sien 'n kasteel.", "kasteel"), ("Die wind waai.", "wind"), ("Hy hou die pikhouweel.", "pikhouweel")]),
        exB=dict(title="Skryf self 'n naamwoord wat pas.", mode="word", items=[
            ("'n Persoon in jou klas:", "Enige naam"), ("'n Plek waar jy graag speel:", "Enige plek"),
            ("'n Ding in jou skoolsak:", "Enige ding"), ("'n Dier:", "Enige dier")]),
        spell=["bus", "eiland", "berge", "rivier", "kasteel", "maat", "wind", "grond"],
        writing="Jy is op die bus! Skryf 5 sinne oor waar jy gaan land en wat jy daar gaan doen. Gebruik ten minste 5 naamwoorde.",
    ),
    # ------------------------------------------------------------------ 2
    dict(
        title="Die Landing",
        key="Werkwoorde",
        story=[
            "Daniel en Lisa val deur die lug. Hulle trek die sambreel oop en sweef stadig af. Daniel land eerste op die dak van 'n groot huis.",
            "Hy hardloop na binne en soek 'n kis. Lisa klim in 'n boom en kyk rond. “Ek sien 'n ander speler!” fluister sy. “Pasop, Daniel!”",
            "Daniel buk en sluip stil agter 'n muur. Sy hart klop vinnig. Dan hoor hy 'n bekende stem: “Moenie bang wees nie, dis net Pieter!” Almal lag.",
        ],
        vocab=[("sambreel", "dit hou jou stadig in die lug"), ("fluister", "baie sag praat"),
               ("sluip", "stil en stadig loop"), ("bekende", "iemand wat jy ken")],
        questions=[
            ("Hoe kom Daniel en Lisa stadig na onder?", "Met die sambreel.", False),
            ("Waar land Daniel?", "Op die dak van 'n groot huis.", False),
            ("Waarin klim Lisa?", "In 'n boom.", False),
            ("Wat doen Daniel agter die muur?", "Hy buk en sluip stil.", False),
            ("Hoekom dink jy lag almal aan die einde?", "Open vraag – bv. omdat dit net Pieter was.", True),
        ],
        tf=[("Daniel land in 'n boom.", False), ("Daniel soek 'n kis.", True), ("Die stem is van Pieter.", True)],
        explain="'n <b>Werkwoord</b> is 'n <b>doenwoord</b>. Dit sê wat iemand of iets <b>doen</b>.<br/>"
                "Voorbeelde: <b>hardloop</b>, <b>klim</b>, <b>kyk</b>, <b>lag</b>.",
        exA=dict(title="Skryf die werkwoord (doenwoord) in elke sin neer.", mode="word", items=[
            ("Daniel hardloop na die huis.", "hardloop"), ("Lisa klim in die boom.", "klim"),
            ("Die bus vlieg weg.", "vlieg"), ("Ek soek 'n kis.", "soek"),
            ("Hulle sweef af.", "sweef"), ("Die speler sluip stil.", "sluip")]),
        exB=dict(title="Kies die regte werkwoord uit die blokkie.", mode="blank",
                 bank=["spring", "bou", "kyk", "lag", "eet", "gly"], items=[
            ("Daniel ________ uit die bus.", "spring"), ("Lisa ________ 'n hoë muur.", "bou"),
            ("Ons ________ na die kaart.", "kyk"), ("Die kinders ________ lekker.", "lag"),
            ("Ek ________ my aandete.", "eet"), ("Die sambreel laat ons stadig ________.", "gly")]),
        spell=["sambreel", "dak", "hardloop", "soek", "klim", "fluister", "sluip", "stil"],
        writing="Jy land op die eiland! Beskryf wat jy doen. Gebruik ten minste 5 werkwoorde en onderstreep elkeen.",
    ),
    # ------------------------------------------------------------------ 3
    dict(
        title="Die Skatkis",
        key="Byvoeglike naamwoorde",
        story=[
            "In die groot huis vind Daniel 'n blink, goue kis. “Dis 'n baie spesiale kis!” sê hy. Stadig maak hy die deksel oop.",
            "Binne lê 'n sterk skild, 'n swaar pikhouweel en 'n klein, rooi gesondheidpakkie. Daniel is baie bly. “Kyk wat ek gekry het!” roep hy.",
            "Lisa kom vinnig aangehardloop. Sy het ook nuttige dinge gevind. Pieter wys sy nuwe, blou rugsak. “Ons span is gereed!” sê hulle saam.",
        ],
        vocab=[("deksel", "die deel wat 'n kis toemaak"), ("skild", "dit beskerm jou"),
               ("nuttig", "iets wat help"), ("gereed", "reg om te begin")],
        questions=[
            ("Hoe lyk die kis?", "Blink en goud.", False),
            ("Noem twee dinge wat in die kis was.", "Enige twee: skild, pikhouweel, gesondheidpakkie.", False),
            ("Watter kleur is die gesondheidpakkie?", "Rooi.", False),
            ("Watter kleur is Pieter se rugsak?", "Blou.", False),
            ("Wat sou jy graag in 'n skatkis wou vind?", "Open vraag.", True),
        ],
        tf=[("Die pikhouweel is lig.", False), ("Die skild is sterk.", True), ("Lisa stap stadig.", False)],
        explain="'n <b>Byvoeglike naamwoord</b> sê <b>hoe iets lyk of voel</b>. Dit staan by 'n naamwoord.<br/>"
                "Voorbeelde: 'n <b>groot</b> bus, 'n <b>rooi</b> kis, 'n <b>sterk</b> skild.",
        exA=dict(title="Skryf die byvoeglike naamwoord in elke sin neer.", mode="word", items=[
            ("Die kis is blink.", "blink"), ("Daniel het 'n sterk skild.", "sterk"),
            ("Die pikhouweel is swaar.", "swaar"), ("Lisa is 'n vinnige hardloper.", "vinnige"),
            ("Die pakkie is klein.", "klein"), ("Ons het 'n mooi dag.", "mooi")]),
        exB=dict(title="Voeg self 'n byvoeglike naamwoord by.", mode="blank", items=[
            ("Die ________ bus vlieg bo die eiland.", "Enige byvoeglike naamwoord"),
            ("Daniel dra 'n ________ rugsak.", "Enige byvoeglike naamwoord"),
            ("Ek het 'n ________ kis gevind.", "Enige byvoeglike naamwoord"),
            ("Die ________ storm kom nader.", "Enige byvoeglike naamwoord"),
            ("Pieter is 'n ________ maat.", "Enige byvoeglike naamwoord")]),
        spell=["blink", "goud", "sterk", "swaar", "klein", "spesiaal", "skild", "deksel"],
        writing="Stel jou voor jy vind jou droomkis! Skryf 6 sinne oor wat daarin is. Gebruik ten minste 5 byvoeglike naamwoorde.",
    ),
    # ------------------------------------------------------------------ 4
    dict(
        title="Die Fort",
        key="Verkleinwoorde",
        story=[
            "Die span soek hout, klip en metaal. “Kom ons bou 'n fort!” sê Daniel. Hy bou 'n sterk muur en Lisa maak 'n dak.",
            "Pieter bou 'n klein muurtjie voor die deur. Hy maak ook 'n trappie sodat hulle op die dakkie kan klim. Binne sit Lisa 'n bankie en 'n tafeltjie neer.",
            "'n Voëltjie sit op 'n klippie en kyk hoe hulle werk. “Ons fort is klaar!” sê Daniel. Almal is trots.",
        ],
        vocab=[("fort", "'n sterk gebou wat jou beskerm"), ("metaal", "'n harde materiaal soos yster"),
               ("trots", "baie tevrede met jouself"), ("klaar", "niks meer om te doen nie")],
        questions=[
            ("Wat soek die span?", "Hout, klip en metaal.", False),
            ("Wie maak die dak?", "Lisa.", False),
            ("Wat bou Pieter voor die deur?", "'n Klein muurtjie.", False),
            ("Waarvoor is die trappie?", "Sodat hulle op die dakkie kan klim.", False),
            ("Hoe sal jou droomfort lyk?", "Open vraag.", True),
        ],
        tf=[("Die voëltjie sit op 'n klippie.", True), ("Daniel bou die fort alleen.", False), ("Pieter maak 'n trappie.", True)],
        explain="'n <b>Verkleinwoord</b> maak iets <b>klein</b>. Ons sit <b>-tjie, -ie, -pie, -kie</b> of <b>-jie</b> agter die woord.<br/>"
                "huis → <b>huisie</b> &nbsp; boom → <b>boompie</b> &nbsp; kar → <b>karretjie</b> &nbsp; dak → <b>dakkie</b>",
        exA=dict(title="Skryf die verkleinwoord.", mode="word", items=[
            ("kis", "kissie"), ("dak", "dakkie"), ("boom", "boompie"), ("kar", "karretjie"),
            ("muur", "muurtjie"), ("klip", "klippie"), ("ster", "sterretjie"), ("huis", "huisie")]),
        exB=dict(title="Skryf die woord weer groot (sonder -tjie, -ie of -pie).", mode="word", items=[
            ("voëltjie", "voël"), ("trappie", "trap"), ("bankie", "bank"), ("tafeltjie", "tafel"),
            ("boekie", "boek"), ("hondjie", "hond")]),
        spell=["fort", "hout", "klip", "metaal", "muurtjie", "dakkie", "trappie", "voëltjie"],
        writing="Jy het 'n klein huisie in die fort gebou. Beskryf dit! Gebruik ten minste 5 verkleinwoorde.",
    ),
    # ------------------------------------------------------------------ 5
    dict(
        title="Die Storm",
        key="Meervoude",
        story=[
            "Skielik word die lug donker. 'n Groot, pers storm kom nader! “Hardloop!” roep Lisa. Die wolke trek saam en die wind waai harder.",
            "Daniel, Lisa en Pieter hardloop oor berge en riviere. Hulle sien drie karre langs die pad. “Spring in!” sê Pieter. Die kinders klim in en ry vinnig weg. Agter hulle waai die storm die bome om.",
            "Naby 'n klein dorpie stop hulle. Daar is baie kiste, en die spelers kry nuwe skilde. Net betyds! Die storm bly agter hulle.",
        ],
        vocab=[("skielik", "baie vinnig, sonder waarskuwing"), ("betyds", "nie te laat nie"),
               ("naby", "nie ver nie"), ("pad", "waar karre ry")],
        questions=[
            ("Hoe lyk die storm?", "Groot en pers.", False),
            ("Oor wat hardloop die span?", "Berge en riviere.", False),
            ("Hoeveel karre sien hulle?", "Drie.", False),
            ("Wat waai die storm om?", "Die bome.", False),
            ("Hoe sal jy voel as 'n storm op jou afkom?", "Open vraag.", True),
        ],
        tf=[("Die lug word helder.", False), ("Pieter sê hulle moet in die karre spring.", True), ("Hulle vind kiste by die dorpie.", True)],
        explain="<b>Meervoud</b> beteken <b>meer as een</b>. Die meeste woorde kry <b>-e</b>, <b>-s</b> of <b>-ers</b> agter.<br/>"
                "berg → <b>berge</b> &nbsp; speler → <b>spelers</b> &nbsp; kind → <b>kinders</b><br/>"
                "Let op! Sommige woorde verander: boom → <b>bome</b>, ster → <b>sterre</b>, bus → <b>busse</b>.",
        exA=dict(title="Skryf die meervoud.", mode="word", items=[
            ("berg", "berge"), ("rivier", "riviere"), ("kar", "karre"), ("boom", "bome"),
            ("kis", "kiste"), ("speler", "spelers"), ("wolk", "wolke"), ("kind", "kinders")]),
        exB=dict(title="Vul die meervoud van die woord in hakies in.", mode="blank", items=[
            ("Daar is baie ________ (boom) in die bos.", "bome"),
            ("Die ________ (speler) wag vir die bus.", "spelers"),
            ("Ons sien twee ________ (kar) in die pad.", "karre"),
            ("Die ________ (ster) skyn in die nag.", "sterre"),
            ("Daar is drie ________ (kis) in die huis.", "kiste"),
            ("Die ________ (wolk) is donker.", "wolke")]),
        spell=["skielik", "storm", "wolke", "betyds", "naby", "pad", "dorpie", "skilde"],
        writing="Jy is in 'n storm! Skryf 5 sinne oor wat jy sien, hoor en doen. Gebruik ten minste 4 meervoude.",
    ),
    # ------------------------------------------------------------------ 6
    dict(
        title="Spanwerk",
        key="Teenoorgestelde",
        story=[
            "In die fort maak die span 'n plan. “Ek is vinnig, maar Pieter is stadig,” sê Lisa. Pieter lag. “Ja, maar ek is sterk, en jy is nog klein!”",
            "Daniel hou nie van terg nie. “Elkeen van ons is goed met iets anders,” sê hy. “Lisa hardloop vinnig en kyk ver. Pieter bou hoog en sterk. Ek hou van die kaart en die plan.”",
            "Die span lyk nou gelukkig, nie hartseer nie. Een gaan buite en kyk of dit veilig is, terwyl die ander binne bly. Spanwerk maak die span sterk!",
        ],
        vocab=[("terg", "vir die grap iemand ontstel"), ("elkeen", "almal, een vir een"),
               ("veilig", "sonder gevaar"), ("spanwerk", "saamwerk as 'n span")],
        questions=[
            ("Wie is vinnig?", "Lisa.", False),
            ("Wie is sterk?", "Pieter.", False),
            ("Hoe voel Daniel oor terg?", "Hy hou nie daarvan nie.", False),
            ("Wat sê Daniel van almal in die span?", "Elkeen is goed met iets anders.", False),
            ("Waarmee is jy goed? Hoe kan dit jou span of gesin help?", "Open vraag.", True),
        ],
        tf=[("Lisa sê Pieter is stadig.", True), ("Daniel hou van terg.", False), ("Een gaan buite en een bly binne.", True)],
        explain="<b>Teenoorgestelde</b> woorde beteken die <b>omgekeerde</b> van mekaar.<br/>"
                "groot ↔ <b>klein</b> &nbsp; dag ↔ <b>nag</b> &nbsp; bly ↔ <b>hartseer</b>",
        exA=dict(title="Skryf die teenoorgestelde.", mode="word", items=[
            ("vinnig", "stadig"), ("groot", "klein"), ("hoog", "laag"), ("bly", "hartseer"),
            ("binne", "buite"), ("nuut", "oud"), ("oop", "toe"), ("warm", "koud")]),
        exB=dict(title="Vul die teenoorgestelde in.", mode="blank", items=[
            ("Die storm is gevaarlik, maar die fort is ________.", "veilig"),
            ("Ek is vandag bly, maar gister was ek ________.", "hartseer"),
            ("Die kis was toe, maar nou is dit ________.", "oop"),
            ("Die pikhouweel is swaar, maar die sambreel is ________.", "lig"),
            ("Die berg is hoog, maar die dal is ________.", "laag"),
            ("Ons gaan op, maar dan gaan ons weer ________.", "af")]),
        spell=["terg", "elkeen", "ruil", "veilig", "spanwerk", "stadig", "hartseer", "buite"],
        writing="Skryf 'n storietjie van 5 sinne oor 'n span wat saamwerk. Gebruik ten minste 3 pare teenoorgestelde woorde.",
    ),
    # ------------------------------------------------------------------ 7
    dict(
        title="Gister se Spel",
        key="Verlede tyd",
        story=[
            "Gister het Daniel en sy span 'n lang spel gespeel. Hulle het hard gewerk. Lisa het die kaart gesoek en Pieter het 'n brug gebou.",
            "Daniel het hoog geklim en ver gekyk. “Ek sien die laaste storm!” het hy geroep. Die span het vinnig gehardloop en agter 'n rots gewag.",
            "Op die ou end het hulle gewen! Hulle het saam gelag en Daniel het gesê: “Ek het die beste span in die wêreld!”",
        ],
        vocab=[("brug", "dit laat jou oor water loop"), ("rots", "'n baie groot klip"),
               ("laaste", "daar is nie meer na hierdie een nie"), ("op die ou end", "uiteindelik")],
        questions=[
            ("Wanneer het die spel plaasgevind?", "Gister.", False),
            ("Wat het Lisa gesoek?", "Die kaart.", False),
            ("Wat het Pieter gebou?", "'n Brug.", False),
            ("Waar het die span gewag?", "Agter 'n rots.", False),
            ("Wat is jou gunsteling deel van die storie? Hoekom?", "Open vraag.", True),
        ],
        tf=[("Die storie het gister gebeur.", True), ("Pieter het die kaart gesoek.", False), ("Die span het gewen.", True)],
        explain="Ons gebruik <b>verlede tyd</b> as iets <b>klaar gebeur het</b>. Ons sê <b>het</b> en sit <b>ge-</b> voor die werkwoord.<br/>"
                "Nou: Ek <b>speel</b>. &nbsp; Gister: Ek <b>het gespeel</b>.",
        exA=dict(title="Skryf die sin in die verlede tyd.", mode="line", items=[
            ("Daniel bou 'n fort.", "Daniel het 'n fort gebou."),
            ("Lisa soek die kaart.", "Lisa het die kaart gesoek."),
            ("Pieter klim in die boom.", "Pieter het in die boom geklim."),
            ("Ons wag by die huis.", "Ons het by die huis gewag."),
            ("Die span kyk na die storm.", "Die span het na die storm gekyk."),
            ("Ek speel saam met my maat.", "Ek het saam met my maat gespeel.")]),
        exB=dict(title="Skryf die verlede tyd van die werkwoord in hakies.", mode="blank", items=[
            ("Ek het gister 'n storm ________ (hoor).", "gehoor"),
            ("Pieter het die fort ________ (maak).", "gemaak"),
            ("Ons het saam ________ (werk).", "gewerk"),
            ("Lisa het my ________ (roep).", "geroep"),
            ("Daniel het 'n skat ________ (sien).", "gesien"),
            ("Die kinders het buite ________ (speel).", "gespeel")]),
        spell=["gister", "gespeel", "gewerk", "geklim", "gewag", "gesoek", "brug", "rots"],
        writing="Skryf in die verlede tyd oor jou laaste dag by die skool of by die huis. Skryf 5 sinne en gebruik “het” en “ge-”.",
    ),
    # ------------------------------------------------------------------ 8
    dict(
        title="Die Soektog",
        key="Voorsetsels",
        story=[
            "Daniel kry 'n geheime kaart. Daarop staan: “Die skat lê tussen twee berge.” Die span begin soek.",
            "Lisa kyk onder die bome. Pieter klim bo-op 'n rots. Daniel loop langs die rivier. Skielik sien hulle 'n kis agter 'n groot klip! Dit staan tussen twee berge.",
            "“Dis dit!” skree Daniel en hardloop daarheen. Hy maak die kis oop. Daar is 'n briefie in: “Goed gedoen! Die beste skat is julle span.” Almal glimlag.",
        ],
        vocab=[("geheime", "iets wat niemand mag weet nie"), ("skat", "iets baie kosbaar"),
               ("briefie", "'n kort boodskap op papier"), ("glimlag", "lag sonder geluid")],
        questions=[
            ("Wat kry Daniel?", "'n Geheime kaart.", False),
            ("Waar lê die skat volgens die kaart?", "Tussen twee berge.", False),
            ("Waar kyk Lisa?", "Onder die bome.", False),
            ("Waar was die kis?", "Agter 'n groot klip.", False),
            ("Wat dink jy is die beste skat? Hoekom?", "Open vraag.", True),
        ],
        tf=[("Pieter klim op 'n rots.", True), ("Daniel loop langs die rivier.", True), ("Die kis is in die bos.", False)],
        explain="'n <b>Voorsetsel</b> sê <b>waar</b> iets is.<br/>"
                "Voorbeelde: <b>op, onder, langs, agter, voor, tussen, in, bo</b>.",
        exA=dict(title="Kies die regte voorsetsel uit die blokkie.", mode="blank",
                 bank=["op", "onder", "langs", "agter", "voor", "tussen", "bo", "in"], items=[
            ("Die voël sit ________ die dak.", "op"), ("Die mol woon ________ die grond.", "onder"),
            ("Daniel staan ________ Lisa, heel naby haar.", "langs"),
            ("Pieter skuil ________ die groot boom.", "agter"),
            ("Die kis is ________ die twee berge.", "tussen"),
            ("Die voëls vlieg ________ die wolke.", "bo"),
            ("Daniel klim ________ die kar.", "in"),
            ("Lisa staan eerste, ________ die ander.", "voor")]),
        exB=dict(title="Skryf 'n sin met elke voorsetsel.", mode="line", items=[
            ("op", "Enige goeie sin."), ("onder", "Enige goeie sin."), ("langs", "Enige goeie sin."), ("agter", "Enige goeie sin.")]),
        spell=["geheime", "skat", "tussen", "langs", "agter", "onder", "briefie", "glimlag"],
        writing="Jy het 'n skatkaart gemaak! Skryf 5 sinne wat vertel waar die skat versteek is. Gebruik ten minste 4 voorsetsels.",
    ),
    # ------------------------------------------------------------------ 9
    dict(
        title="Nie Opgee Nie",
        key="Ontkenning",
        story=[
            "In die laaste ronde kom die span in 'n moeilike plek. “Ek is nie bang nie,” sê Daniel, maar sy hande bewe.",
            "“Ons het nie baie skilde nie,” sê Lisa. “En die storm is nie ver nie.” Pieter skud sy kop. “Ons gaan nie opgee nie! Ons het nog nie verloor nie!”",
            "Daniel haal diep asem. “Ek sien nie 'n ander speler nie, so ons het tyd om te bou.” Hulle werk saam. Die fort is nie perfek nie, maar dit is sterk genoeg.",
        ],
        vocab=[("moeilike", "nie maklik nie"), ("bewe", "skud van skrik of koue"),
               ("asem", "die lug wat jy in en uit blaas"), ("perfek", "sonder foute")],
        questions=[
            ("Hoekom is die span in 'n moeilike plek?", "Hulle het nie baie skilde nie en die storm is naby.", False),
            ("Wat sê Daniel oor bang wees?", "Hy sê hy is nie bang nie.", False),
            ("Wie sê hulle gaan nie opgee nie?", "Pieter.", False),
            ("Wat doen die span met die tyd wat hulle het?", "Hulle bou saam.", False),
            ("Skryf oor 'n keer toe jy nie opgegee het nie.", "Open vraag.", True),
        ],
        tf=[("Daniel sê hy is bang.", False), ("Pieter wil opgee.", False), ("Die fort is sterk genoeg.", True)],
        explain="In Afrikaans gebruik ons gewoonlik <b>twee nies</b>: <b>nie ... nie</b>.<br/>"
                "Ek is bly. → Ek is <b>nie</b> bly <b>nie</b>.",
        exA=dict(title="Maak die sin ontkennend (gebruik nie ... nie).", mode="line", items=[
            ("Daniel is bly.", "Daniel is nie bly nie."),
            ("Lisa hou van die storm.", "Lisa hou nie van die storm nie."),
            ("Hulle het 'n kaart.", "Hulle het nie 'n kaart nie."),
            ("Ons wil wen.", "Ons wil nie wen nie."),
            ("Die bus is leeg.", "Die bus is nie leeg nie."),
            ("Pieter kan swem.", "Pieter kan nie swem nie.")]),
        exB=dict(title="Daar is een fout in elke sin. Skryf die sin reg.", mode="line", items=[
            ("Ek is nie moeg.", "Ek is nie moeg nie."),
            ("Hulle het nie 'n fort.", "Hulle het nie 'n fort nie."),
            ("Lisa sien nie die kis.", "Lisa sien nie die kis nie."),
            ("Die span gee nie op.", "Die span gee nie op nie.")]),
        spell=["bang", "opgee", "moeilike", "bewe", "asem", "perfek", "verloor", "genoeg"],
        writing="Skryf 5 sinne oor dinge wat jy nie wil doen nie. Gebruik die twee nies (nie ... nie) in elke sin.",
    ),
    # ------------------------------------------------------------------ 10
    dict(
        title="Die Nuwe Speler",
        key="Vrae stel",
        story=[
            "'n Nuwe speler, Sipho, sluit by die span aan. Hy is skaam, maar hy het baie vrae. “Wie is die leier?” vra hy.",
            "“Dis Daniel,” sê Lisa. “Hoekom?” vra Sipho. “Want hy luister altyd na almal,” antwoord Pieter. “Waar gaan ons land?” vra Sipho. “By die dorp,” sê Daniel. “Wanneer begin die volgende spel?” “Môre om tien!”",
            "“Hoe leer ek bou?” vra Sipho. “Ek wys jou,” sê Daniel. “Wat maak jy as jy bang is?” “Ek haal diep asem en bly kalm,” sê Daniel. Sipho glimlag. Nou is hy deel van die span.",
        ],
        vocab=[("skaam", "bang om met mense te praat"), ("leier", "die een wat die span lei"),
               ("luister", "aandag gee met jou ore"), ("kalm", "rustig")],
        questions=[
            ("Wie is die nuwe speler?", "Sipho.", False),
            ("Hoekom is Daniel die leier?", "Hy luister altyd na almal.", False),
            ("Waar gaan hulle land?", "By die dorp.", False),
            ("Wanneer begin die volgende spel?", "Môre om tien.", False),
            ("Watter vraag sou jy vir Sipho vra?", "Open vraag.", True),
        ],
        tf=[("Sipho is nie skaam nie.", False), ("Daniel wys vir Sipho hoe om te bou.", True), ("Die spel begin vanmiddag.", False)],
        explain="Ons gebruik <b>vraagwoorde</b> om vrae te vra: <b>Wie?</b> (persoon) <b>Wat?</b> (ding) <b>Waar?</b> (plek) "
                "<b>Wanneer?</b> (tyd) <b>Hoekom?</b> (rede) <b>Hoe?</b> (manier).<br/>"
                "'n Vraag eindig altyd met 'n <b>vraagteken (?)</b>.",
        exA=dict(title="Kies die regte vraagwoord uit die blokkie.", mode="blank",
                 bank=["Wie", "Wat", "Waar", "Wanneer", "Hoekom", "Hoe"], items=[
            ("________ is jou maat? – Lisa is my maat.", "Wie"),
            ("________ staan die kis? – In die huis.", "Waar"),
            ("________ begin die spel? – Môre om tien.", "Wanneer"),
            ("________ is jy bly? – Want ons het gewen!", "Hoekom"),
            ("________ maak Daniel? – Hy bou 'n fort.", "Wat"),
            ("________ vinnig kan jy hardloop? – Baie vinnig!", "Hoe")]),
        exB=dict(title="Skryf 'n vraag wat by die antwoord pas.", mode="line", items=[
            ("Antwoord: Ek is nege jaar oud.", "Hoe oud is jy?"),
            ("Antwoord: Dis Daniel.", "Wie is die leier? (of ’n soortgelyke vraag)"),
            ("Antwoord: Ons land by die dorp.", "Waar land julle?"),
            ("Antwoord: Want dit is lekker.", "Hoekom hou jy daarvan?")]),
        spell=["wie", "wat", "waar", "wanneer", "hoekom", "leier", "luister", "kalm"],
        writing="Skryf 5 vrae wat jy vir 'n nuwe maat wil vra. Begin elke vraag met 'n ander vraagwoord en eindig met 'n vraagteken.",
    ),
    # ------------------------------------------------------------------ 11
    dict(
        title="Die Brief",
        key="Hoofletters en leestekens",
        story=[
            "Daniel skryf 'n brief aan sy nuwe maat, Sipho:",
            "Liewe Sipho,",
            "Dankie dat jy by ons span aangesluit het! Ons het vandag baie pret gehad. Ek het hout, klip en metaal gebêre. Lisa, Pieter en ek wil môre weer speel. Kom jy saam?",
            "Groete,<br/>Daniel",
        ],
        vocab=[("aangesluit", "deel geword van 'n groep"), ("gebêre", "veilig weggesit"),
               ("groete", "'n manier om 'n brief af te sluit"), ("pret", "'n lekker tyd")],
        questions=[
            ("Aan wie skryf Daniel die brief?", "Aan Sipho.", False),
            ("Waarvoor bedank Daniel hom?", "Dat hy by die span aangesluit het.", False),
            ("Wat het Daniel gebêre?", "Hout, klip en metaal.", False),
            ("Watter vraag vra Daniel aan die einde?", "Kom jy saam?", False),
            ("Aan wie sal jy graag 'n brief skryf? Hoekom?", "Open vraag.", True),
        ],
        tf=[("Die brief begin met “Liewe Sipho”.", True), ("Daniel het die dinge verloor.", False), ("Daniel wil nie weer speel nie.", False)],
        explain="<b>Hoofletter</b>: aan die begin van 'n sin en by name (Daniel, Suid-Afrika).<br/>"
                "<b>Punt (.)</b> aan die einde van 'n sin. &nbsp; <b>Vraagteken (?)</b> by 'n vraag. &nbsp; <b>Uitroepteken (!)</b> by 'n bevel of opgewondenheid.<br/>"
                "<b>Komma (,)</b> in 'n lys: Ek het hout<b>,</b> klip en metaal.",
        exA=dict(title="Skryf oor met hoofletters en leestekens.", mode="line", items=[
            ("daniel en lisa speel saam", "Daniel en Lisa speel saam."),
            ("waar is die kaart", "Waar is die kaart?"),
            ("pasop vir die storm", "Pasop vir die storm!"),
            ("ek het hout klip en metaal", "Ek het hout, klip en metaal."),
            ("pieter bou 'n fort", "Pieter bou 'n fort."),
            ("hoekom is jy bly", "Hoekom is jy bly?")]),
        exB=dict(title="Kies die regte leesteken ( .  ?  !  , ) en skryf dit op die lyn.", mode="blank", items=[
            ("Hoe oud is jy ____", "?"), ("Ek sien 'n bus ____ 'n kar en 'n fiets.", ","),
            ("Kyk uit ____", "!"), ("Ons gaan môre speel ____", "."),
            ("Waar is Lisa ____", "?"), ("Die storm kom ____", "!  (of .)")]),
        spell=["brief", "liewe", "dankie", "groete", "pret", "gebêre", "hoofletter", "leesteken"],
        writing="Skryf 'n brief aan 'n maat. Begin met “Liewe ...” en eindig met “Groete”. Gebruik hoofletters en leestekens reg.",
    ),
    # ------------------------------------------------------------------ 12
    dict(
        title="Die Groot Wenner",
        key="Skryf jou eie storie",
        story=[
            "Dis die laaste ronde! Net twee spanne is nog oor. Die storm word al kleiner, en Daniel se hart klop vinnig.",
            "“Onthou, ons werk saam,” sê Daniel. Lisa kyk na die kaart en wys die pad. Pieter bou 'n hoë, sterk fort. Sipho kyk uit vir gevaar. Daniel praat sag met almal.",
            "Dan gebeur dit! Die lug word helder en groot letters verskyn: “OORWINNING!” Die span spring op en af van blydskap. “Ons het dit gedoen!” skree Daniel. “Ons het nooit opgegee nie.”",
            "Daniel leer iets belangriks: lees en skryf is soos oefen vir 'n spel. Hoe meer jy oefen, hoe beter word jy. Nou is dit jou beurt om 'n storie te skryf!",
        ],
        vocab=[("blydskap", "baie groot geluk"), ("belangrik", "iets wat saak maak"),
               ("oefen", "iets oor en oor doen om beter te word"), ("oorwinning", "wanneer jy wen")],
        questions=[
            ("Hoeveel spanne is nog oor?", "Twee.", False),
            ("Wat doen Pieter?", "Hy bou 'n hoë, sterk fort.", False),
            ("Watter woord verskyn aan die einde?", "OORWINNING.", False),
            ("Wat leer Daniel?", "Hoe meer jy oefen, hoe beter word jy.", False),
            ("Hoe sal jy jou eie storie begin?", "Open vraag.", True),
        ],
        tf=[("Die span het opgegee.", False), ("Sipho kyk uit vir gevaar.", True), ("Die span het gewen.", True)],
        explain="'n Goeie storie het 'n <b>begin</b> (wie en waar), 'n <b>middel</b> (wat gebeur) en 'n <b>einde</b> (hoe dit eindig).<br/>"
                "Nuttige woorde: <b>eers, toe, daarna, uiteindelik</b>.",
        exA=dict(title="Beplan jou storie. Skryf kort antwoorde.", mode="line", items=[
            ("Wie is die hoofkarakter?", "Enige antwoord."), ("Waar speel dit af?", "Enige antwoord."),
            ("Wat is die probleem?", "Enige antwoord."), ("Hoe word die probleem opgelos?", "Enige antwoord."),
            ("Hoe eindig die storie?", "Enige antwoord.")]),
        exB=dict(title="Sit die sinne in die regte volgorde. Skryf net die letters.", mode="none", items=[
            ("a)  Hulle het die spel gewen.", ""), ("b)  Daniel en sy span het in die bus gesit.", ""),
            ("c)  Die storm het begin kom.", ""), ("d)  Hulle het die fort gebou.", ""),
            ("Volgorde: ________________________", "b, c, d, a")]),
        spell=["oorwinning", "blydskap", "belangrik", "oefen", "einde", "begin", "middel", "eindig"],
        writing="Skryf jou eie storie van minstens 10 sinne. Gee dit 'n titel!",
        long_writing=True,
    ),
]

# ------------------------------------------------------------------ woordsoeke
WORDSEARCH = [
    (3, "Woordsoek 1", ["BUS", "EILAND", "BERGE", "KASTEEL", "WIND", "GROND", "BLINK", "GOUD", "STERK", "SWAAR"]),
    (6, "Woordsoek 2", ["FORT", "HOUT", "KLIP", "METAAL", "STORM", "WOLKE", "TERG", "ELKEEN", "RUIL", "VEILIG"]),
    (9, "Woordsoek 3", ["GISTER", "BRUG", "ROTS", "SKAT", "TUSSEN", "LANGS", "AGTER", "BANG", "ASEM", "PERFEK"]),
    (12, "Woordsoek 4", ["WANNEER", "HOEKOM", "LEIER", "KALM", "BRIEF", "GROETE", "PRET", "OEFEN", "EINDE", "BEGIN"]),
]

# ------------------------------------------------------------------ toetse
# (na hoofstuk, titel, vrae, dikteewoorde)  vraag = (teks, opsies|None, antwoord)
TESTS = [
    (4, "Toets Jouself 1 (Vlak 1 – 4)", [
        ("Watter woord is 'n naamwoord?", ["hardloop", "kasteel", "sterk"], "kasteel"),
        ("Watter woord is 'n werkwoord?", ["klim", "blou", "berg"], "klim"),
        ("Kies die byvoeglike naamwoord: 'n ________ kis.", ["blink", "loop", "dorp"], "blink"),
        ("Wat is die verkleinwoord van “dak”?", ["dakke", "dakkie", "dakker"], "dakkie"),
        ("Wat is die verkleinwoord van “kar”?", ["karretjie", "karrie", "karre"], "karretjie"),
        ("Skryf een sin met 'n naamwoord, 'n werkwoord en 'n byvoeglike naamwoord.", None, "Open – bv. Die sterk speler bou 'n fort."),
    ], ["sambreel", "eiland", "hardloop", "spesiaal", "voëltjie"]),
    (8, "Toets Jouself 2 (Vlak 5 – 8)", [
        ("Wat is die meervoud van “berg”?", ["berge", "bergs", "bergers"], "berge"),
        ("Wat is die meervoud van “speler”?", ["speler", "spelers", "spelere"], "spelers"),
        ("Wat is die teenoorgestelde van “stadig”?", ["lank", "vinnig", "klein"], "vinnig"),
        ("Wat is die teenoorgestelde van “veilig”?", ["gevaarlik", "gelukkig", "sterk"], "gevaarlik"),
        ("Skryf in die verlede tyd: Ek bou 'n fort.", None, "Ek het 'n fort gebou."),
        ("Kies die voorsetsel: Die kis is ________ die twee berge.", ["tussen", "op", "vinnig"], "tussen"),
    ], ["skielik", "betyds", "geheime", "glimlag", "gespeel"]),
    (12, "Toets Jouself 3 (Vlak 9 – 12)", [
        ("Maak ontkennend: Lisa is bang.", None, "Lisa is nie bang nie."),
        ("Kies die vraagwoord: ________ is jy vandag so bly?", ["Hoekom", "Wie", "Waar"], "Hoekom"),
        ("Skryf reg: waar is pieter", None, "Waar is Pieter?"),
        ("Watter leesteken kom aan die einde? Pasop vir die storm ____", ["?", "!", ","], "!"),
        ("Kies die verlede tyd:", ["Ek het gewerk.", "Ek werk.", "Ek sal werk."], "Ek het gewerk."),
        ("Waar of vals? 'n Storie het 'n begin, 'n middel en 'n einde.", ["Waar", "Vals"], "Waar"),
    ], ["oorwinning", "belangrik", "moeilike", "liewe", "pret"]),
]
