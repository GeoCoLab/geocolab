<template>
  <p>GeoCoLab aims to evidence and address the hypothesis that access to analytical facilities by underserved researchers is a key issue that leads to a deep inequality in environmental research and determines who is able to generate environmental and geoscience knowledge.</p>
</template>

<script setup>
</script>

<style lang="scss">
@import 'scss/vars';

// display the subtitle and make the title bigger
#header {
  height: 200px;

  & .site-subtitle {
    display: block;
    font-size: 1.25rem;
  }
}

@media (min-width: $break-sm) {
  #header {
    & .site-title {
      font-size: 4.5rem;
    }

    & .site-subtitle {
      font-size: 1.5rem;
    }
  }
}
</style>
