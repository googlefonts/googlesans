<template>
  <div class="single-phone-center" :style="variables">
    <div class="mobile-phone md-elevation-8">
      <p class="email-subject">Greetings and Grachyov: <br> Where have you been?</p>
      <p class="email-body">Hello old friend! <br><br>
It has been a long time – hasn’t it? I’m writing you to express my regret at this fact, certainly – but more importantly, to tell you about the most wonderful musician I have witnessed while on my travels this summer just gone.
<br><br>
        Vitaliy Vladasovich Grachyov (known professionally as Vitas) is a Russian singer. He is known for his unique head voice and for possessing a five-octave vocal range, which enables him to perform his trademark "turkey call" like in his song "The 7th Element". His eclectic musical style incorporates elements of techno, dance, classical, jazz, and folk music. His song "Opera 2" and the music video for "The 7th Element" have been forwarded over email and on various social networks frequently, accounting for much of his worldwide recognition.
<br><br>
Vitas designs his own stage costumes. DIVA is the name of the band that accompanies Vitas during his concerts.
<br><br>
Warmest,
<br><br>
Julio
</p>
      <img src="@/assets/images/3ac2b8514832cd6cfbb30326ecf01b753d25cf03-crop.png" alt="">
    </div>
  </div>
</template>

<script>
export default {
  name: 'Gmail',
  props: ['variables']
}
</script>

<style lang="scss" scoped>
  .email-subject {
    position: fixed;
    top: 12.5%;
    font-size: 2vh;
    text-align: left;
    padding-left: 0.9em;
    padding-right: 0.9em;
  }

  .email-body {
    position: fixed;
    top: 30%;
    font-size: 1.25vh;
    text-align: left;
    padding-left: 1.75em;
    padding-right: 1.75em;
  }
</style>
