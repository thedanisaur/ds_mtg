# Design

## Ablities, Keywords, & Types

### Keywords

```
Existing:
- Flying
- First Strike
- Double Strike
- Vigilance
- Reach
- Trample
- Lifelink
- Indestructible (Effects that say destroy do not destroy this.)
- Haste
- Protection
- Prowess (Whenever you cast a noncreature spell, this creature gets +1/+1 until end of turn.)
- Shadow (This creature can block or be blocked by only creatures with shadow.)

New:
- Accursed
- Bleed
- Fragment
- Plague
- Soullink
```

Default order should be: Flash, defender, flying, first strike, double strike, vigilance, reach, trample, menace, deathtouch, lifelink, hexproof, indestructible, haste, protection, prowess, *accursed*, *bleed*, *plague*, *soullink*.

### Abilities

```
- Accursed (When a creature or planeswalker is dealt damage by a source with accursed, that permanent also gets a curse counter for each damage received. Permanents with curse counters have, "At the beginning of your upkeep, if this permanent has a number of curse counters greater than or equal to its mana value, sacrifice it. Otherwise remove a curse counter." When a player is dealt damage by a source with accursed, they create a Curse token.)
- Bleed (Whenever you have 5, plus the number of Moss Clump tokens you control, or more bleed counters, you take that much damage. You remove all bleed counters and create a Moss Clump token. (It's an artifact with "{1}, {T}, Sacrifice this artifact: You gain 2 life and get two souls. Scry 2."))
- Chameleon (You may cast this card face down as a 1/1 colorless Hollow creature for {1}. Turn it face up any time for its chameleon cost.)
- Fragment (While searching your library, you may reveal this card from your library and pay [cost]. If you do, [effect]. Only one fragment ability may be used per search.)
- Kindle (You may pay a number of souls equal to this card's converted mana cost, if you do transform it. Activate this ability only anytime you could cast a sorcery.)
- Plague (If a creature or player would be dealt damage by a source with plague, instead that creature or player gets a plague counter for each damage received.)
Infuse {X} (You may cast this spell for its infuse cost or activate this ability on the battlefield. If you do, this enchantment loses enchant creature and gains enchant equipment, then loses this ability. Attach it to target equipment. Then the enchanted equipment gains the abilities of this enchantment, except instead of "enchanted creature" it says "equipped creature")
- Soullink (Damage dealt by this creature also causes you to get that many souls.)
```

#### New Rules

```
Accursed

- a) Accursed is a static ability.
- b) Damage dealt by a source with accursed causes a player that is dealt that damage to create that many curse tokens.
- c) Damage marked onto a permanent by a source with accursed also causes that source’s controller to put that many curse counters on that permanent.
    - 1) As long as a permanent has a curse counter on it that permanent has, "At the beginning of your upkeep, if this permanent has a number of curse counters greater than or equal to its mana value, sacrifice it. Otherwise remove a curse counter from it."
- d) If an object changes zones before an effect causes it to deal damage, its last known information is used to determine whether it had accursed.
- e) The accursed rules function no matter what zone an object with accursed deals damage from.
- f) Multiple instances of accursed on the same object are redundant.
- g) Reminder text: When a creature or planeswalker is dealt damage by a source with accursed, that permanent also gets a curse counter for each damage received. Permanents with curse counters have, "At the beginning of your upkeep, if this permanent has a number of curse counters greater than or equal to its mana value, sacrifice it. Otherwise remove a curse counter." When a player is dealt damage by a source with accursed, they create a Curse token.
```

```
Bleed

- a) Bleed is a static ability
- b) Damage dealt by a source with bleed causes a player that is dealt that damage to get that many bleed counters.
    - 1) As long as a player has atleast one bleed counter that player has an emblem with "Whenever you have 5, plus the number of Moss Clump tokens you control, or more bleed counters, you take that much damage. Then you remove all bleed counters and create a Moss Clump token. (It's an artifact with "{1}, {T}, Sacrifice this artifact: You gain 2 life and get two souls. Scry 2.")"
    - 2) If a player has no bleed counters their bleed emblem ceases to exist.
    - 3) A player may only have one bleed emblem at a time.
- c) If an object changes zones before an effect causes it to deal damage, its last known information is used to determine whether it had bleed.
- d) The bleed rules function no matter what zone an object with bleed deals damage from.
- e) Multiple instances of bleed on the same object are redundant.
- f) Reminder text: If a player would be dealt damage by a source with bleed, they also get a bleed counter for each damage received
```

```
Fragment

- a) Fragment is a keyword ability that functions while a card with fragment is in a library. "Fragment [cost] — [effect]" means "While searching your library, you may reveal this card from your library. If you do, pay [cost]. When you do, [effect]."
- b) A fragment ability may be used only while its owner is searching their library. (It goes on the stack while searching and will resolve after the search is complete)
- c) A player can't use more than one fragment ability during a single library search.
- d) Revealing a card for a fragment ability doesn't inherently remove it from the library.
- e) Reminder text: While searching your library, you may reveal this card from your library and pay [cost]. If you do, [effect]. Only one fragment ability may be used per search
```

```
Infuse

- a) Infuse is an keyword ability of Aura cards that functions in a player's hand and on the battlefield.
    - 1) In the player's hand, any time that player could cast a sorcery they may cast a card with infuse.
        - 1a) “Infuse [cost]” means “You may pay [cost] rather than pay this spell's mana cost anytime you could cast a sorcery. If you do, this enchantment loses enchant creature and gains enchant equipment, then loses this ability. The enchanted equipment gains the abilities of this enchantment, except instead of 'enchanted creature' it says 'equipped creature'.”
    - 2) On the battlefield, any time that player could cast a sorcery they may activate this ability.
        - 2a) “Infuse [cost]” means “[Cost]: This enchantment loses enchant creature and gains enchant equipment, then loses this ability. Attach this permanent to target equipment. The enchanted equipment gains the abilities of this enchantment, except instead of 'enchanted creature' it says 'equipped creature'. Activate only as a sorcery.”
- c) Activating the Infuse ability results in a text changing effect (see rule 612, Text-Changing Effects).
- d) Reminder text: You may cast this spell for its infuse cost or activate this ability on the battlefield. If you do, this enchantment loses enchant creature and gains enchant equipment, then loses this ability. The enchanted equipment gains the abilities of this enchantment, except instead of "enchanted creature" it says "equipped creature"
```

```
Plague (similar in function to 702.90. Infect)

- a) Plague is a static ability.
- b) Damage dealt to a player by a source with plague doesn’t cause that player to lose life. Rather, it causes that source’s controller to give the player that many plague counters. See rule 120.3b to infer how to deal with this change.
    - 1) As long as a player has atleast one plague counter that player has an emblem with "If you would be dealt damage prevent that damage and you recieve that many plague counters instead. At the beginning of each end step this emblem deals damage to you equal to the number of plague counters you have, then remove a plague counter."
    - 2) If a player has no plague counters their plague emblem ceases to exist.
    - 3) A player may only have one plague emblem at a time.
- c) Damage dealt to a creature by a source with plague isn’t marked on that creature. Rather, it causes that source’s controller to put that many plague counters on that creature. See rule 120.3d to infer how to deal with this change.
    - 1) As long as a creature has a plague counter on it that creature has, "If this creature is dealt damage it gets a plague counter. At the beginning of each end step deal X damage to this creature where X is the number of plague counters on it, then remove a plague counter from it."
- d) If an object changes zones before an effect causes it to deal damage, its last known information is used to determine whether it had plague.
- e) The plague rules function no matter what zone an object with plague deals damage from.
- f) Multiple instances of plague on the same object are redundant.
- g) Reminder text: If a creature or player would be dealt damage by a source with plague, instead that creature or player gets a plague counter for each damage received
```


```
Soullink

- a) Soullink is a static ability
- b) Damage dealt by a source with soullink causes a player that is dealt that damage to get that many soul counters.
- c) If an object changes zones before an effect causes it to deal damage, its last known information is used to determine whether it had soullink.
- d) The soullink rules function no matter what zone an object with soullink deals damage from.
- e) Multiple instances of soullink on the same object are redundant.
- f) Reminder text: Damage dealt by this creature also causes you to get that many souls
```

### Card types

Supertypes:
```
Bonfire
```

Subtypes:

```
Fragment
Hag
Hollow
Infusion
Lord
Moss Clump
Soul
```

## Sets

### Dark Souls (DKS) Card Distribution

Count

```
Cards 255
Tokens 16
Basics 6
Total 277
```

Type Distribution

```
10 colorless cards
35 white cards
35 blue cards
35 black cards
35 red cards
35 green cards
25 gold cards
30 artifact cards
15 nonbasic lands
06 basic lands
16 tokens
```

Rarity Distribution
```
102 common
80 uncommon
55 rare
18 mythic
```

Booster distribution
```
- 11 commons
- 3 uncommons
- 1 rare
- 1 in 8 rare is replaced with mythic
- 1 land slot
```

### Lost Crowns of the Kings (LCK) Card Distribution

Count

```
Cards 304
Tokens 14
Basics 6
Total 324
```

Type Distribution

```
07 colorless cards
42 white cards
42 blue cards
42 black cards
42 red cards
42 green cards
14 gold cards
40 artifact cards
33 nonbasic lands
06 basic lands
14 tokens
```

Rarity Distribution
```
145 common
82 uncommon
58 rare
19 mythic
```

### The Fire Fades (TFF) Card Distribution

TBD

# Set Lists

Dark Souls set list - [DKS](dks.md)

Lost Crowns of the Kings set list - [LCK](lck.md)

The Fire Fades set list - [TFF](tff.md)