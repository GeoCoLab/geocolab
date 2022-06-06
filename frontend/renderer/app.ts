import { createSSRApp, defineComponent, h, markRaw, reactive } from 'vue';
import PageShell from './PageShell.vue';
import type { Component, PageContext } from '../types';
import { setPageContext } from '../utils/usePageContext';

// extensions
import { createPinia, setActivePinia } from 'pinia/dist/pinia';
import { useEnumStore } from '../store/enums';
import { useFormStore } from '../store/forms';
import { useAuthStore } from '../store/auth';
import { defaultConfig as formKitConfig, plugin as formKit } from '@formkit/vue';
import { generateClasses } from '@formkit/themes';
import VueFeather from 'vue-feather';
import Help from '../components/Help.vue';
import CountrySelect from '../components/CountrySelect.vue';
import CurrencySelect from '../components/CurrencySelect.vue';

const pinia = createPinia();
setActivePinia(pinia);

// init enums
const enumStore = useEnumStore();
enumStore.init();

// init forms
const formStore = useFormStore();
formStore.init();

// try and load user
const authStore = useAuthStore();
authStore.loadUser();

export { createApp };

function createApp(pageContext: PageContext) {
    const {Page} = pageContext;

    let rootComponent: Component;
    const PageWithWrapper = defineComponent({
        data: () => ({
            Page: markRaw(Page),
            pageProps: markRaw(pageContext.pageProps || {})
        }),
        created() {
            rootComponent = this;
        },
        render() {
            return h(
                PageShell,
                {},
                {
                    default: () => {
                        return h(this.Page, this.pageProps);
                    }
                }
            );
        }
    });

    const app = createSSRApp(PageWithWrapper);

    app.use(pinia);

    app.component('vue-feather', VueFeather);
    app.component('help', Help);
    app.component('country-select', CountrySelect);
    app.component('currency-select', CurrencySelect)

    objectAssign(app, {
        changePage: (pageContext: PageContext) => {
            Object.assign(pageContextReactive, pageContext);
            rootComponent.Page = markRaw(pageContext.Page);
            rootComponent.pageProps = markRaw(pageContext.pageProps || {});
        }
    });

    const pageContextReactive = reactive(pageContext);

    app.use(formKit, formKitConfig({
        config: {
            classes: generateClasses({
                checkbox: {
                    wrapper: 'input-first'
                },
                submit: {
                    input: '$reset formkit-button'
                }
            })
        }
    }));

    setPageContext(app, pageContextReactive);

    return app;
}

function objectAssign<Obj, ObjAddendum>(obj: Obj, objAddendum: ObjAddendum): asserts obj is Obj & ObjAddendum {
    Object.assign(obj, objAddendum);
}
