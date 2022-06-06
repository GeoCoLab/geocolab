<template>
  <div class="help">
    <vue-feather type="help-circle" @mouseover="showText=true" @mouseout="showText=false"/>
    <span class="help-text ml-2" v-if="showText">
      <slot />
    </span>
  </div>
</template>

<script setup>
import { ref } from 'vue';

let showText = ref(false);
</script>

<style scoped lang="scss">
@import 'scss/vars';

.help {
  font-size: 0.9em;
  text-align: right;
  line-height: 1em;
}

.help-text {
  margin-top: 0.3em;
}

@media (min-width: $break-md) {
  .help-text {
    position: absolute;
    width: max-content;
    max-width: 25em;
  }
}
</style>
