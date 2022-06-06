<template>
<div class="h-full w-full grid gap-2 items-center relative" :class="col ? 'grid-flow-row' : 'grid-flow-col'">
  <slot>
    <NavItem v-for="l in props.links" v-bind="l" :direction="col ? 'right' : 'down'"/>
  </slot>
</div>
</template>

<script setup>
import NavItem from './NavItem.vue';
import { computed } from 'vue';

const props = defineProps(['links', 'direction'])

const col = computed(() => props.direction === 'col');
</script>

<style scoped>

</style>
