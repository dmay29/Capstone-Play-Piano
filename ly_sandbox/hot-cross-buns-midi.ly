% Lily was here -- automatically converted by midi2ly from hot-cross-buns.mid
\version "2.24.3"

\layout {
  indent = 0.0
  \context {
    \Voice
    \remove Note_heads_engraver
    \consists Completion_heads_engraver
    \remove Rest_engraver
    \consists Completion_rest_engraver
  }
}

trackAchannelA = {


  \key g \major
    
  \time 4/4 
  

  \key g \major
  
  \tempo 4 = 125 
  
  \set Staff.instrumentName = "Greensleeves"
  
  % [TEXT_EVENT] Traditional
  
  % [COPYRIGHT_NOTICE] Jim Paterson
  \skip 4*1/256 
}

trackA = <<
  \context Voice = voiceA \trackAchannelA
>>


trackBchannelA = {
  
  \set Staff.instrumentName = "Piano"
  \skip 128*1021 
}

trackBchannelB = \relative c {
  \voiceOne
  d''4*244/256 r4*12/256 d,4*244/256 r4*12/256 <g g, b >4*487/256 
  r4*25/256 
  | % 2
  d'4*244/256 r4*12/256 d,4*244/256 r4*12/256 <g g, b >4*487/256 
  r4*25/256 
  | % 3
  d'4*122/256 r4*6/256 c4*122/256 r4*6/256 b4*122/256 r4*6/256 a4*122/256 
  r4*6/256 g4*122/256 r4*6/256 a4*122/256 r4*6/256 b4*122/256 r4*6/256 c4*122/256 
  r4*6/256 
  | % 4
  d4*244/256 r4*12/256 d,4*244/256 r4*12/256 g4*244/256 r4*12/256 g4*122/256 
  r4*6/256 g4*122/256 r4*6/256 
  | % 5
  d'4*122/256 r4*6/256 d4*122/256 r4*6/256 d4*122/256 r4*6/256 d4*122/256 
  r4*6/256 c4*244/256 r4*12/256 c4*244/256 r4*12/256 
  | % 6
  b4*122/256 r4*6/256 b4*122/256 r4*6/256 b4*122/256 r4*6/256 b4*122/256 
  r4*6/256 <a d,, fis >4*487/256 r4*25/256 
  | % 7
  d4*122/256 r4*6/256 c4*122/256 r4*6/256 b4*122/256 r4*6/256 a4*122/256 
  r4*6/256 g4*122/256 r4*6/256 a4*122/256 r4*6/256 b4*122/256 r4*6/256 c4*122/256 
  r4*6/256 
  | % 8
  d4*244/256 r4*12/256 d,4*244/256 r4*12/256 <g g, b >4*487/256 
}

trackBchannelBvoiceB = \relative c {
  \voiceTwo
  <d a' > r4*537/256 
  | % 2
  <d a' >4*487/256 r4*537/256 
  | % 3
  <b g' >4*487/256 r4*25/256 <b d >4*487/256 r4*25/256 
  | % 4
  <d a' >4*487/256 r4*25/256 <g b >4*487/256 r4*25/256 
  | % 5
  <b, g' >4*487/256 r4*25/256 <c g' >4*487/256 r4*25/256 
  | % 6
  <d g >4*487/256 r4*537/256 
  | % 7
  <b g' >4*487/256 r4*25/256 <b d >4*487/256 r4*25/256 
  | % 8
  <d a' >4*487/256 
}

trackB = <<
  \context Voice = voiceA \trackBchannelA
  \context Voice = voiceB \trackBchannelB
  \context Voice = voiceC \trackBchannelBvoiceB
>>


\score {
  <<
    \context Staff=trackB \trackA
    \context Staff=trackB \trackB
  >>
  \layout {
    \context {
      \Staff
      \remove Instrument_name_engraver
    }
  }
  \midi {}
}
