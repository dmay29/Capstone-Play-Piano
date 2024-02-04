% Lily was here -- automatically converted by /usr/bin/midi2ly from mary_little_lamb.mid
\version "2.14.0"

\layout {
  \context {
    \Voice
    \remove "Note_heads_engraver"
    \consists "Completion_heads_engraver"
    \remove "Rest_engraver"
    \consists "Completion_rest_engraver"
  }
}

trackAchannelA = {
  
  \time 4/4 
  
  \tempo 4 = 55 
  
  \set Staff.instrumentName = "Elec. Piano (Classic)"
  
}

trackAchannelB = \relative c {
  e16 d c d e e e r16 d d d r16 e g g r16 
  | % 2
  e d c d e e e r16 d d e d c 
}

trackA = <<

  \clef bass
  
  \context Voice = voiceA \trackAchannelA
  \context Voice = voiceB \trackAchannelB
>>


\score {
  <<
    \context Staff=trackA \trackA
  >>
  \layout {}
  \midi {}
}
