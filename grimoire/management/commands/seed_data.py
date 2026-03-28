"""
Management command: python manage.py seed_data
Populates the database with sample plants, posts, categories, etc.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from blog.models import Category, Tag, Series, Post
from grimoire.models import Plant, PlantFamily, PlantProperty, ObservationLog


class Command(BaseCommand):
    help = 'Seed the database with sample botanical data'

    def handle(self, *args, **options):
        self.stdout.write('🌿 Seeding Botanica database...')

        # ── Admin user ────────────────────────────────────────────────
        if not User.objects.filter(username='admin').exists():
            user = User.objects.create_superuser('admin', 'admin@botanica.local', 'botanica2024')
            user.first_name = 'The'
            user.last_name = 'Botanist'
            user.save()
            self.stdout.write('  ✓ Created admin user (admin / botanica2024)')
        else:
            user = User.objects.get(username='admin')

        # ── Plant Families ────────────────────────────────────────────
        families_data = [
            ('Lamiaceae', 'Mint family'),
            ('Asteraceae', 'Daisy family'),
            ('Rosaceae', 'Rose family'),
            ('Apiaceae', 'Carrot family'),
            ('Fabaceae', 'Legume family'),
            ('Solanaceae', 'Nightshade family'),
        ]
        families = {}
        for name, common in families_data:
            f, _ = PlantFamily.objects.get_or_create(name=name, defaults={'common_name': common})
            families[name] = f

        # ── Plant Properties ──────────────────────────────────────────
        props_data = [
            ('Medicinal', 'use'), ('Edible', 'use'), ('Aromatic', 'quality'),
            ('Toxic', 'use'), ('Dye plant', 'use'), ('Pollinator', 'quality'),
            ('Shade tolerant', 'habitat'), ('Wetland', 'habitat'),
            ('Alpine', 'habitat'), ('Spring', 'season'), ('Summer', 'season'),
            ('Autumn', 'season'), ('Evergreen', 'season'),
        ]
        props = {}
        for name, cat in props_data:
            p, _ = PlantProperty.objects.get_or_create(name=name, defaults={'category': cat})
            props[name] = p

        # ── Plants ────────────────────────────────────────────────────
        plants_data = [
            {
                'scientific_name': 'Lavandula angustifolia',
                'common_names': 'Lavender, English Lavender, True Lavender',
                'family': 'Lamiaceae',
                'order': 'Lamiales',
                'genus': 'Lavandula',
                'species': 'angustifolia',
                'edibility': 'edible',
                'overview': (
                    'Lavandula angustifolia is among the most beloved aromatic herbs in the world — '
                    'a small, woody perennial native to the Mediterranean basin that has found its way '
                    'into gardens, medicine cabinets, and kitchens across every continent. '
                    'Its silvery-green foliage and spires of violet-blue flowers have made it a symbol '
                    'of calm, cleanliness, and healing across cultures.'
                ),
                'morphology': (
                    'A dense, rounded subshrub reaching 30–60 cm in height. Leaves are narrow, '
                    'linear, 2–6 cm long, with margins that roll under, and covered in fine grey-white '
                    'hairs that give the plant its characteristic silver hue. Flower spikes rise 20–40 cm '
                    'above the foliage on long, slender stems. Flowers are small, tubular, purple to violet, '
                    'and arranged in interrupted whorls around the stem.'
                ),
                'habitat': (
                    'Native to rocky, dry, well-drained soils at altitude — mountainous regions of the '
                    'Mediterranean, from Spain and France through to the Balkans. It thrives in full sun '
                    'with low rainfall and poor, alkaline soils. In cultivation, it adapts to most '
                    'temperate climates given adequate drainage.'
                ),
                'distribution': 'Native Mediterranean; widely naturalised and cultivated globally.',
                'bloom_season': 'June – August',
                'uses_medicinal': (
                    'Lavender oil is the most extensively researched essential oil in aromatherapy. '
                    'Studies support its use for anxiety reduction, improved sleep quality, and mild '
                    'analgesic effects. Topically, it has antimicrobial and anti-inflammatory properties, '
                    'and is commonly applied to burns, insect bites, and minor wounds. The dried flowers '
                    'are used as a nerve tonic in traditional herbalism.'
                ),
                'uses_culinary': (
                    'Flowers and leaves are edible and used to flavour baked goods, syrups, honey, '
                    'teas, and savoury dishes. Lavender sugar, lavender shortbread, and herbes de Provence '
                    '(which classically includes lavender) are well-known applications. Use sparingly — '
                    'the flavour is intense and can become soapy if overdone.'
                ),
                'preparation_methods': (
                    'Infusion (tea): 1 tsp dried flowers per cup, steep 5–10 min.\n'
                    'Essential oil: steam distillation of fresh flower spikes.\n'
                    'Tincture: flowers in 40% alcohol for 4–6 weeks.\n'
                    'Topical: dilute essential oil 2% in carrier oil (e.g. jojoba) before skin use.'
                ),
                'field_notes': (
                    'I first encountered wild lavender on the limestone garrigue above Montpellier, '
                    'in early July when the heat rose from the rocks in waves. The scent was nothing '
                    'like the bottles I had known — richer, resinous, and underlaid with something '
                    'almost mineral. The bees were extraordinary in their industry.'
                ),
                'locations_observed': 'Montpellier garrigue, France. Cotswold garden, UK. Nyahururu plateau, Kenya.',
                'seasonal_patterns': 'Flowers from June in lower altitudes; peaks July–August in mountains. Silver foliage visible year-round.',
                'symbolism': (
                    'Lavender has been associated with cleanliness (the name derives from Latin lavare, '
                    'to wash), calm, and female healing knowledge. In Victorian flower language it '
                    'signified devotion and mistrust in equal measure.'
                ),
                'personal_reflections': (
                    'There is something about the convergence of colour and scent in lavender that defies '
                    'easy analysis. It is simultaneously the most cultivated and the most wild-feeling of '
                    'herbs — domesticated into rows yet retaining something austere and ancient in its '
                    'grey-green habit.'
                ),
                'properties': ['Medicinal', 'Edible', 'Aromatic', 'Pollinator', 'Summer'],
            },
            {
                'scientific_name': 'Achillea millefolium',
                'common_names': 'Yarrow, Common Yarrow, Milfoil, Nosebleed Plant',
                'family': 'Asteraceae',
                'order': 'Asterales',
                'genus': 'Achillea',
                'species': 'millefolium',
                'edibility': 'medicinal',
                'overview': (
                    'Achillea millefolium is one of the great wound herbs of the Northern Hemisphere — '
                    'used from the Bronze Age to the present day to staunch bleeding and clean injury. '
                    'Named for the hero Achilles who is said to have staunched his soldiers\' wounds with '
                    'it, yarrow is a plant of remarkable ubiquity and generous medicine.'
                ),
                'morphology': (
                    'An erect perennial 30–90 cm tall with deeply divided, feathery leaves that give '
                    'the species epithet millefolium (thousand leaves). The stems are slightly woolly '
                    'and tough. Flowers are borne in flat-topped corymbs of tiny white to pale pink '
                    'ray florets, each cluster 2–4 mm across, giving a lacy, meadow quality.'
                ),
                'habitat': (
                    'Exceptionally versatile — roadsides, meadows, wasteland, lawns, forest edges, '
                    'and alpine grassland to 3,500 m. Prefers well-drained, moderately fertile soils '
                    'in full to partial sun. Drought-tolerant once established.'
                ),
                'distribution': 'Circumpolar across the Northern Hemisphere; naturalised worldwide.',
                'bloom_season': 'June – September',
                'uses_medicinal': (
                    'The archetypal wound herb. Contains achilleic acid which promotes blood clotting; '
                    'also anti-inflammatory, diaphoretic (promotes sweating in fever), bitter tonic for '
                    'digestion, and mild urinary antiseptic. Used internally for colds and fever, '
                    'menstrual regulation, and digestive complaints.'
                ),
                'preparation_methods': (
                    'Fresh leaves: applied directly to wounds to staunch bleeding.\n'
                    'Tea: 2 tsp dried herb per cup, steep 10 min — for fever, digestion.\n'
                    'Tincture: 1:5 in 40% alcohol.\n'
                    'Oil infusion: good base for wound-healing salves.'
                ),
                'warnings': (
                    'Avoid in pregnancy (uterine stimulant). Can cause contact dermatitis in sensitive '
                    'individuals. Avoid in people with ragweed allergy. Do not confuse with similar-looking '
                    'species in Apiaceae (carrot family), some of which are toxic.'
                ),
                'field_notes': (
                    'Yarrow appears wherever the land has been disturbed. I have found it on Nairobi '
                    'roadsides, in Alpine meadows, beside Scottish lochans. It is a plant of resilience, '
                    'choosing the margins and the edges, the unglamorous corners where few herbs bother.'
                ),
                'locations_observed': 'Naivasha, Kenya. Cairngorms, Scotland. Dolomites, Italy.',
                'seasonal_patterns': 'Basal leaves present year-round; flowering stems appear June onwards.',
                'symbolism': 'The plant of Achilles; associated with military courage and the art of healing wounds — physical and otherwise.',
                'properties': ['Medicinal', 'Pollinator', 'Summer', 'Autumn'],
            },
            {
                'scientific_name': 'Rosa canina',
                'common_names': 'Dog Rose, Wild Briar, Briar Rose',
                'family': 'Rosaceae',
                'order': 'Rosales',
                'genus': 'Rosa',
                'species': 'canina',
                'edibility': 'edible',
                'overview': (
                    'Rosa canina is perhaps the most ancient cultivated rose — the foundation stock '
                    'from which centuries of garden cultivation have grown. It is a plant of hedgerows '
                    'and woodland margins, indifferent to soil or attention, extravagant in autumn '
                    'with its glossy crimson hips.'
                ),
                'morphology': (
                    'A vigorous deciduous shrub, 2–5 m, with arching stems armed with strong, curved '
                    'prickles. Leaves pinnate, 5–7 leaflets, slightly glossy, margins toothed. '
                    'Flowers 5-petalled, pale to deep pink or white, 4–5 cm, with yellow stamens. '
                    'Hips (rose hips) oval to elongated, 1.5–2 cm, turning brilliant scarlet in autumn.'
                ),
                'habitat': 'Hedgerows, scrubby woodland edges, chalk downland, road verges. Tolerates poor soils.',
                'distribution': 'Europe, Western Asia, Northwest Africa. Naturalised worldwide.',
                'bloom_season': 'May – July (flowers); September – February (hips)',
                'uses_medicinal': (
                    'Rose hips are among the richest plant sources of Vitamin C — weight for weight '
                    'containing 20× more than oranges. Hips used traditionally and in modern practice '
                    'for immune support, joint inflammation, and as a general nutritive tonic. '
                    'Also a source of Vitamins A, B, E, K and lycopene.'
                ),
                'uses_culinary': (
                    'Hips make excellent syrup, jelly, jam, wine, tea, and soup. Petals are edible '
                    'and can be crystallised, added to salads, or used to flavour vinegar and honey. '
                    'The seed achenes inside the hip are hairy and should be removed before eating.'
                ),
                'preparation_methods': (
                    'Rose hip syrup: simmer hips, strain out seeds and hairs carefully, cook with sugar.\n'
                    'Hip tea: 2 tbsp dried hips per cup, simmer 20 min, strain well.\n'
                    'Petal infusion: fresh petals, hot water, steep 5 min. Add honey.'
                ),
                'field_notes': (
                    'Dog rose hips in November, after the first frost when they soften — this is '
                    'the moment. The sweetness is unlike anything cultivated. I gather them along '
                    'the Limuru escarpment every year, always with the feeling of finding something '
                    'the rest of the world has forgotten.'
                ),
                'locations_observed': 'Limuru Road hedgerows, Kenya. South Downs, England. Tuscany.',
                'seasonal_patterns': 'Flowers May–July; hips ripen September–October; persist through winter.',
                'symbolism': (
                    'The rose has accumulated more symbolism than perhaps any other plant: love, beauty, '
                    'transience, secrecy (sub rosa), passion and thorn. The dog rose specifically carries '
                    'the wilder, older associations — the rose before cultivation refined it into something '
                    'more legible.'
                ),
                'personal_reflections': (
                    'There is a recklessness to Rosa canina that cultivated roses have lost. It climbs '
                    'where it wishes, takes what light it can find, and in October produces something '
                    'frankly astonishing — those blood-red hips against grey sky, which are both fruit '
                    'and warning.'
                ),
                'properties': ['Medicinal', 'Edible', 'Aromatic', 'Pollinator', 'Summer', 'Autumn'],
            },
            {
                'scientific_name': 'Urtica dioica',
                'common_names': 'Stinging Nettle, Common Nettle, Nettle',
                'family': 'Urticaceae',
                'edibility': 'edible',
                'overview': (
                    'One of the most nutritionally dense plants available freely in the temperate world. '
                    'Nettle is maligned for its sting and overlooked as a result — but those who know it '
                    'regard it as one of the most generously useful plants in any flora. Eaten in spring, '
                    'drunk as tea, applied medicinally, used as fibre: the nettle gives without reserve.'
                ),
                'morphology': (
                    'Erect perennial, 50–150 cm. Stems square in cross-section, covered in hollow '
                    'stinging hairs (trichomes) that inject formic acid, histamine, and serotonin. '
                    'Leaves opposite, cordate to lanceolate, margins deeply serrate. Flowers small, '
                    'green, drooping catkins — dioecious (separate male/female plants).'
                ),
                'habitat': 'Disturbed ground, riverbanks, woodland margins, gardens. Indicates nitrogen-rich soil.',
                'distribution': 'Cosmopolitan across temperate regions worldwide.',
                'bloom_season': 'June – September',
                'uses_medicinal': (
                    'Rich in iron, calcium, magnesium, Vitamins A, C, K. Used as a tonic herb for '
                    'anaemia, fatigue, and general debility. Root preparations used for benign '
                    'prostatic hyperplasia. Anti-inflammatory, used topically for joint pain (urtication).'
                ),
                'uses_culinary': (
                    'Young leaves (before flowering, or wearing gloves) cooked like spinach — '
                    'soups, pestos, risottos, nettle tea, beer. Heat destroys the sting. '
                    'One of the most iron-rich greens available and entirely free, all spring.'
                ),
                'uses_other': 'Fibre from stems used to make cloth; a source of green dye; garden liquid feed when composted in water.',
                'preparation_methods': (
                    'Cooking: blanch briefly in boiling water — sting is completely destroyed by heat.\n'
                    'Tea: 1 tbsp fresh or dried leaf per cup, steep 10 min. Nourishing tonic.\n'
                    'Tincture: fresh plant in 25% alcohol.\n'
                    'Topical: fresh leaf applied directly for joint pain (urtication therapy).'
                ),
                'warnings': 'Do not eat raw unless sting is removed first (rolling between palms or pressing firmly). Not recommended in pregnancy in large amounts.',
                'field_notes': (
                    'I have a complicated relationship with nettles — mostly because I spent my '
                    'childhood being stung by them in ignorance, and my adulthood learning to '
                    'cook them in gratitude. The spring flush of young growth is something I now '
                    'wait for each year. The colour when blanched is an impossibly vivid green.'
                ),
                'locations_observed': 'Karura Forest, Nairobi. Almost everywhere with disturbed ground.',
                'seasonal_patterns': 'Best harvested young in spring. Use before flowering for culinary purposes.',
                'properties': ['Medicinal', 'Edible', 'Dye plant', 'Spring', 'Summer'],
            },
        ]

        created_plants = []
        for pd in plants_data:
            props_for_plant = pd.pop('properties', [])
            family_name = pd.pop('family', None)

            plant, created = Plant.objects.get_or_create(
                scientific_name=pd['scientific_name'],
                defaults={**pd, 'created_by': user, 'family': families.get(family_name) if family_name else None}
            )
            if created:
                self.stdout.write(f'  ✓ Created plant: {plant.scientific_name}')

            plant.properties.set([props[p] for p in props_for_plant if p in props])
            created_plants.append(plant)

        # ── Blog Categories ───────────────────────────────────────────
        cats_data = [
            ('Field Studies', 'Direct observations from the field — botanical encounters in the wild.'),
            ('Plant Profiles', 'In-depth explorations of individual species.'),
            ('Essays', 'Reflective and contemplative writing on plants, nature, and knowledge.'),
            ('Recipes & Preparations', 'Putting botanical knowledge into practice.'),
        ]
        categories = {}
        for name, desc in cats_data:
            c, _ = Category.objects.get_or_create(name=name, defaults={'description': desc})
            categories[name] = c

        # ── Tags ──────────────────────────────────────────────────────
        tag_names = ['aromatics', 'woodland', 'hedgerow', 'medicinal', 'foraging', 'kenya', 'scotland', 'spring', 'autumn', 'healing']
        tags = {}
        for tn in tag_names:
            t, _ = Tag.objects.get_or_create(name=tn)
            tags[tn] = t

        # ── Series ────────────────────────────────────────────────────
        s1, _ = Series.objects.get_or_create(
            name='Field Reflections',
            defaults={'description': 'Personal encounters with plants in their wild habitats — part journal, part science, part wonder.'}
        )
        s2, _ = Series.objects.get_or_create(
            name='Plant Studies',
            defaults={'description': 'Deep dives into individual plants: their botany, ethnobotany, and personal significance.'}
        )

        # ── Posts ─────────────────────────────────────────────────────
        posts_data = [
            {
                'title': 'On the Lavender of the Garrigue',
                'excerpt': 'There is a version of lavender that exists beyond bottles and sachets — wild, resinous, mineral. I found it on the limestone hills above Montpellier in early July.',
                'body': '''It was mid-morning when I climbed above the last vineyard and the landscape changed.

The maquis gave way to something older and more austere — a garrigue of limestone rock and low, grey-green shrubs. The heat was already serious. Cicadas made the air seem to vibrate.

And then the lavender.

Not the rows of cultivated lavender that have become the cliché of Provence — but scattered plants choosing their own positions among the rocks, each one low and dense and somehow self-contained. The colour at that distance was a bruised purple, almost grey in the full light.

The scent was the discovery. I have lived with lavender most of my life — in oil, in soap, dried in linen, used clinically. But none of that prepared me for the complexity of the scent when I knelt beside a wild plant in July heat on limestone. There was the familiar floral note, yes, but underneath it something resinous and camphoraceous, and underneath that something mineral — the rock itself, I think, the chalk that makes this landscape and that the plant has been drawing from for centuries.

**What the bottles lose**

Essential oils are the distillation of a plant's aromatic compounds, but they are also a reduction. The context disappears. What does lavender smell like when it is also cicadas and limestone and thirty-five degrees and altitude? When the bees working the flowers are part of the experience?

I spent an hour on that hillside without intention of doing anything useful. This is harder to justify than it sounds. But I think it was necessary — to understand lavender not as an ingredient but as a place.

**On returning**

I brought back only what I had gathered in memory, which is the right amount. The dried flowers I bought in the market were good — but I know now what I am approximating when I use them.

That is enough.''',
                'category': 'Field Studies',
                'tags': ['aromatics', 'medicinal', 'scotland'],
                'series': s1,
                'series_order': 1,
                'plants': ['Lavandula angustifolia'],
                'tone': 'journal',
            },
            {
                'title': 'Yarrow: The Wound Herb of the Wayside',
                'excerpt': 'Achillea millefolium appears wherever the land has been disturbed — a plant of edges, margins, and resilience. And an underappreciated healer.',
                'body': '''Yarrow is a plant of the common places — the verge, the wasteland, the disturbed margin where other plants have not yet settled. This is its genius: wherever humanity moves through the land and disrupts it, yarrow follows, as if in answer to the wounds we leave.

The etymology encodes the connection. Achillea from Achilles, who is said to have staunched his soldiers' wounds with the plant during the Trojan War. Millefolium — a thousand leaves — for the feathery, deeply divided foliage that gives the plant its lacy texture. The folk name "nosebleed plant" for its two uses: to stop nosebleeds, and sometimes to cause them (as a headache remedy in an era when releasing pressure had therapeutic logic).

**In the field**

I have encountered yarrow on three continents without looking for it. That is what it is like — it simply appears. A friend and fellow botanist calls it "the everywhere plant," and there is no better description. I have found it beside Nairobi roads, in Cairngorm meadows at 800 metres, along Italian alpine tracks.

The flowers are impossible to mistake once you know them: flat-topped clusters of tiny, composite flowerheads, each one a miniature daisy in white or pale pink. The smell when you bruise the leaves is characteristic — aromatic, slightly bitter, medicinal in the most direct sense.

**The chemistry of wound healing**

What yarrow does to blood is interesting. It contains achilleic acid (also called achilleine), a compound that promotes platelet aggregation — the initial step in blood clotting. This is why the direct application of crushed fresh leaves to a bleeding wound works, and why it has been used across cultures that never communicated with each other for exactly this purpose.

But yarrow also contains anti-inflammatory compounds (flavonoids, sesquiterpene lactones), volatile oils with antimicrobial activity, and bitter compounds that support digestion. It is a genuinely multi-layered medicinal plant — which is perhaps why it has persisted in use for so long.

**Using it**

The simplest application remains the best: fresh leaves, bruised between the fingers, applied to a wound. Nothing could be more immediate or more direct.

For internal use — particularly the classic use of tea to bring down fever by inducing mild perspiration — the dried herb works well. Two teaspoons per cup, steeped ten minutes. It tastes bitter and aromatic simultaneously, with a pleasant warmth that spreads through the chest.

This is a plant worth knowing. It costs nothing and is found almost everywhere. That combination of accessibility and genuine efficacy is, I think, what the best herbs share.''',
                'category': 'Plant Profiles',
                'tags': ['medicinal', 'foraging', 'kenya'],
                'series': s2,
                'series_order': 1,
                'plants': ['Achillea millefolium'],
                'tone': 'essay',
            },
            {
                'title': 'The Nettle, Reconsidered',
                'excerpt': 'I spent my childhood being stung by nettles and my adulthood learning to cook them. This is a reconsideration — not quite an apology, but something close.',
                'body': '''My childhood relationship with Urtica dioica was one of mutual hostility.

The nettle stood at the edge of every garden, every wasteland, every shortcut through long grass, and it stung without discrimination — bare legs, hands reaching for something else, ankles above too-short socks. I understood it as a pest, a nuisance, a thing to be avoided or cut down.

This understanding took approximately thirty years to fully revise.

**What I missed**

Stinging nettle is among the most nutritious plants growing freely in the temperate world. A single cup of blanched nettle leaves contains more iron than most cuts of beef — and the iron is in a form that human bodies absorb well. It contains calcium, magnesium, Vitamins A, C, and K, and a range of compounds that have genuine anti-inflammatory activity.

It is also, in spring, delicious. This fact surprised me most.

The spring growth — young leaves before the plant has flowered, when they are still small and bright green — blanched briefly and cooked like spinach, becomes something soft, deeply flavoured, and nutty. The sting is entirely destroyed by heat. The colour it turns when blanched is a vivid, electric green that looks almost fabricated.

**On foraging it responsibly**

Wear gloves or use folded newspaper. Take only the top four leaves — this is both the most tender growth and the most sustainable practice. Don't forage near roads (pollution) or near the base of walls where dogs have been. The plants regenerate quickly and can be harvested several times through spring.

**A recipe worth having**

Nettle soup: sauté an onion and a potato in butter. Add a large bag of blanched nettles (strain and roughly chop). Pour over a litre of good stock. Simmer fifteen minutes. Blend, season, finish with cream. Serve with bread.

This is not a recipe you need to adjust or improve. It is exactly as good as it sounds.

**A revision of childhood**

I think what the nettle requires of us is attention before reaction. The sting is real — but it is also entirely avoidable once you know the plant. And what it offers once you look past the defence is extraordinary: free food, free medicine, growing in abundance on land that no one else is using.

That is a generosity worth meeting with more than hostility.''',
                'category': 'Essays',
                'tags': ['foraging', 'spring', 'medicinal'],
                'plants': ['Urtica dioica'],
                'tone': 'essay',
            },
        ]

        plant_lookup = {p.scientific_name: p for p in created_plants}

        for pd in posts_data:
            plants = pd.pop('plants', [])
            tag_names_list = pd.pop('tags', [])
            cat_name = pd.pop('category')
            series_obj = pd.pop('series', None)
            series_order = pd.pop('series_order', None)

            post, created = Post.objects.get_or_create(
                slug=Post(title=pd['title']).slug or __import__('django.utils.text', fromlist=['slugify']).slugify(pd['title']),
                defaults={
                    **pd,
                    'author': user,
                    'status': Post.STATUS_PUBLISHED,
                    'published_at': timezone.now(),
                    'category': categories.get(cat_name),
                    'series': series_obj,
                    'series_order': series_order,
                }
            )
            if not created:
                pass
            else:
                post.tags.set([tags[t] for t in tag_names_list if t in tags])
                post.referenced_plants.set([plant_lookup[p] for p in plants if p in plant_lookup])
                self.stdout.write(f'  ✓ Created post: {post.title}')

        # ── Observation logs ──────────────────────────────────────────
        lavender = plant_lookup.get('Lavandula angustifolia')
        yarrow = plant_lookup.get('Achillea millefolium')

        if lavender and not lavender.observations.exists():
            ObservationLog.objects.create(
                plant=lavender, author=user,
                date='2024-07-04', location='Garrigue above Montpellier, France',
                coordinates='43.6047,3.8722',
                notes='Wild plants on limestone, flowering at peak. Bee activity extraordinary. Scent far more complex than cultivated — resinous, camphoraceous base note.'
            )

        if yarrow and not yarrow.observations.exists():
            ObservationLog.objects.create(
                plant=yarrow, author=user,
                date='2024-09-15', location='Limuru Road verge, Nairobi, Kenya',
                coordinates='-1.2406,36.6552',
                notes='Found growing along roadside verge at ~2100m altitude. Full sun, clay soil. Plants tall (70cm+), robust. Flowering heavily. Collected a small sample.'
            )

        self.stdout.write(self.style.SUCCESS('\n✅ Botanica seeded successfully!'))
        self.stdout.write('   → Admin: http://127.0.0.1:8000/admin/  (admin / botanica2024)')
        self.stdout.write('   → Blog:  http://127.0.0.1:8000/blog/')
        self.stdout.write('   → Grimoire: http://127.0.0.1:8000/grimoire/')
