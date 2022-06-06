<template>
  <div ref="target" @mouseover="toggleDropdown(true)" @mouseout="toggleDropdown(false)"
       class="relative w-full">
    <a class="px-4 py-1 mx-1 grid justify-center items-center w-full"
       :class="[isActive ? 'nav-item--active' : 'nav-item', props.dropdown ? 'has-dropdown' : '']" :href="props.path"
       :aria-expanded="showDropdown"
       :aria-controls="dropdownId">
      <span class="flex items-center">
        <slot>
          {{ props.label }}
        </slot>
      </span>
      <vue-feather :type="arrow" size="1em" @click="toggleDropdown(!showDropdown)" v-if="props.dropdown" />
    </a>
    <Dropdown :id="dropdownId" :show="showDropdown" @toggle-dropdown="toggleDropdown"
              :direction="props.direction" v-if="props.dropdown">
      <NavBlock :links="props.dropdown" direction="col" />
    </Dropdown>
  </div>
</template>

<script setup>
import { onClickOutside, useDebounceFn } from '@vueuse/core';
import { usePageContext } from '../../utils/usePageContext';
import { computed, defineProps, ref } from 'vue';
import Dropdown from './Dropdown.vue';
import NavBlock from './NavBlock.vue';

const pageContext = usePageContext();
const props = defineProps({ path: String, label: String, dropdown: Array, direction: String });

const isActive = computed(() => {
  return pageContext.urlPathname === props.path;
});

const dropdownId = props.path.toLowerCase().replace(/[^a-z\d]/g, '');
const showDropdown = ref(false);
const target = ref(null);
onClickOutside(target, e => {
  showDropdown.value = false;
});

const toggleDropdown = useDebounceFn((state) => {
  if (!props.dropdown) {
    return;
  }
  showDropdown.value = state;
}, 100);

const arrow = computed(() => {
  let suffix;
  switch (props.direction) {
    case 'up':
      suffix = showDropdown.value ? 'down' : 'up';
      break;
    case 'left':
      suffix = showDropdown.value ? 'right' : 'left';
      break;
    case 'right':
      suffix = showDropdown.value ? 'left' : 'right';
      break;
    default:
      // down is default
      suffix = showDropdown.value ? 'up' : 'down';
      break;
  }
  return 'chevron-' + suffix;
});

</script>

<style scoped lang="scss">
.nav-item, .nav-item--active {
  &.has-dropdown {
    grid-template-columns: 1fr minmax(1em, auto);
    grid-gap: 0.25em;
  }

  &:not(.has-dropdown) {
    grid-template-columns: 1fr;
  }
}
</style>
