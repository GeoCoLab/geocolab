<template>
  <h2 class="page-title">Researcher registration</h2>
  <p>GeoCoLab is designed to improve access to analytical facilities for minority and marginalised scientists. The
     following questions will be used to ensure that you meet one or more required criteria. The data collected here
     will additionally be used to evaluate and monitor use of the GeoCoLab app. Data used for this purpose will be
     anonymised and aggregated data may be shared with third parties (e.g. NERC as project funders) and in publications.
     Further details on how this data is collected, stored, used and shared is provided in the GeoCoLab terms and
     conditions.</p>
  <p v-if="(!ediTodo) && (!ediExtraTodo)" class="text-red-500 font-bold text-xl text-center">
    <template v-if="auth.userData.role === 'researcher'">
      You have already completed this step.
    </template>
    <template v-else>
      You do not need to complete this step.
    </template>
  </p>
  <FormKit type="form" v-model="formDataEdi" form-class="mx-auto long-form" submit-label="Save & Continue"
           @submit="submitEdi"
           :errors="errorsEdi" v-if="ediTodo">
    <FormKitSchema :schema="forms.forms.edi"></FormKitSchema>
  </FormKit>
  <template v-if="ediExtraTodo && !ediTodo">
    <p>The following questions will help us understand our users and to evaluate and monitor use of GeoCoLab. Data used
       for this purpose will be anonymised and aggregated data may be shared with third parties (e.g. NERC as project
       funders) and in publications.</p>
    <FormKit type="form" v-model="formDataExtra" form-class="mx-auto long-form" submit-label="Submit"
             @submit="submitExtra"
             :errors="errorsExtra">
      <FormKitSchema :schema="forms.forms.edi_extra"></FormKitSchema>
    </FormKit>
  </template>
</template>

<script setup>
import { computed, ref } from 'vue';
import { navigate } from 'vite-plugin-ssr/client/router';
import { useFormStore } from '../../store/forms';
import { useAuthStore } from '../../store/auth';

const auth = useAuthStore();
const forms = useFormStore();
let errorsEdi = ref([]);
const formDataEdi = ref({});
let errorsExtra = ref([]);
const formDataExtra = ref({});

const submitEdi = async () => {
  forms.submitForm('edi', formDataEdi.value)
       .then(r => {
         if (r.status >= 400) {
           errorsEdi.value = r.data.errors;
         } else {
           auth.loadUser();
         }
       });
};

const submitExtra = async () => {
  forms.submitForm('edi_extra', formDataExtra.value)
       .then(r => {
         if (r.status >= 400) {
           errorsExtra.value = r.data.errors;
         } else {
           navigate('/');
         }
       });
};

const ediTodo = computed(() => {
  return auth.userData.todo.includes('edi');
});

const ediExtraTodo = computed(() => {
  return auth.userData.todo.includes('edi_extra');
});
</script>

<style lang="scss">
</style>
