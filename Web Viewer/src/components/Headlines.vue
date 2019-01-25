<template>
  <div class="main-container">
    <div :style="typefaceStyle" class="text-container big-text google-text">
      <p contenteditable="true" :style="variables">
        Google <br>
        ABCDEFGHIJKLMN <br>
        OPQRSTUVWXYZ <br>
        abcdefghijklmnopq <br>
        rstuvwxyz <br>
        0123456789 <br>
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Headlines',
  props: ['variables', 'typefaceStyle']
}
</script>
