<template>
  <div class="form-editor">
    <div class="flex w-full justify-around">
      <vue-feather type="download-cloud" @click="getSchema" />
      <vue-feather type="arrow-up-circle" @click="displaySchema" />
      <vue-feather type="code" @click="reformat" />
      <vue-feather type="save" @click="saveSchema" :style="{'color': saved ? 'green' : 'red'}" />
    </div>
    <div class="w-full m-4">
      <Codemirror
          v-model="editorContent"
          :style="{ height: '400px' }"
          :autofocus="true"
          :indent-with-tab="true"
          :tabSize="2"
          :extensions="extensions"
          @change="saved = false"
      />
    </div>
  </div>
</template>

<script setup>
import { json } from '@codemirror/lang-json';
import { Codemirror } from 'vue-codemirror';
import { post } from '../utils/api';
import { ref } from 'vue';
import prettier from 'prettier';
import parserJson from 'prettier/parser-babel';
import { useFormStore } from '../store/forms';

const emit = defineEmits(['update:modelValue']);

const props = defineProps(['formName', 'modelValue']);

const forms = useFormStore();
const extensions = [json()];
let editorContent = ref('{}');
const saved = ref(false);

function reformat() {
  try {
    editorContent.value = prettier.format(editorContent.value, { parser: 'json', plugins: [parserJson] });
  } catch (e) {
    console.log(e);
  }
}

function saveSchema() {
  post('/forms/save-fields', {
    form: props.formName,
    fields: props.modelValue
  }).then(r => {
    saved.value = true;
  });
}

function displaySchema() {
  emit('update:modelValue', JSON.parse(editorContent.value));
}

function getSchema() {
  forms.getForm(props.formName).then((f) => {
    editorContent.value = JSON.stringify(f);
    reformat();
    emit('update:modelValue', f);
    saved.value = true;
  }).catch(e => {
    console.log(e);
  });
}
</script>

<style scoped>
.form-editor {
  margin: 4em 2em;
}
</style>
