<template>
  <FormKit type="select" :name="name" :label="label" validation-label="This information" :options="enums.countries" v-model="value" @change="changeValue" />
</template>

<script setup>
import { useEnumStore } from '../store/enums';
import {ref} from 'vue';

const enums = useEnumStore();

const props = defineProps(['modelValue', 'name', 'label']);
const emit = defineEmits(['update:modelValue']);
const value = ref(null)

function changeValue() {
  emit('update:modelValue', value.value)
}
</script>

<style scoped>

</style>
