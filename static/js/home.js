$(function() {
    /* NOTE: hard-refresh the browser once you've updated this */
    $(".typed").typed({
      strings: [
        "stat Noah<br/>" + 
        "><span class='caret'>$</span> Bachelors in Computer Engineering from <a href='https://www.cs.washington.edu/'>the Allen School</a> <br/> ^100"+
        "><span class='caret'>$</span> skills: backend development, embedded systems <br/> ^100" +
        "><span class='caret'>$</span> languages: Java, Python, C, C++, bash, SystemVerilog<br/>" +
        "><span class='caret'>$</span> hobbies: skateboarding, snowboarding, music, dog training, gardening, greenhouse design and construction.<br/> ^300" +
        "><span class='caret'>$</span> <a href= 'mailto:noahstaveley@gmail.com?Subject=Hello%20-from-website'> send me an email <br/>"

        
      ],
      showCursor: true,
      cursorChar: '_',
      autoInsertCss: true,
      typeSpeed: 0.001,
      startDelay: 50,
      loop: false,
      showCursor: false,
      onStart: $('.message form').hide(),
      onStop: $('.message form').show(),
      onTypingResumed: $('.message form').hide(),
      onTypingPaused: $('.message form').show(),
      onComplete: $('.message form').show(),
      onStringTyped: function(pos, self) {$('.message form').show();},
    });
    $('.message form').hide()
  });