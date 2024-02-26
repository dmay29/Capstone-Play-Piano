## To convert a midi file to a lilypond file
`midi2ly FILE_NAME`

## To convert a lilypond file to png
`lilypond -d preview mary_little_lamb-midi.ly`

## How to remove indent
```
\layout {
  indent = 0.0
  ...
}
```

## How to remove Instrument name
```
\score {
 ...
  \layout {
    \context {
      \Staff
      \remove Instrument_name_engraver
    }
  }
  ...
}
```