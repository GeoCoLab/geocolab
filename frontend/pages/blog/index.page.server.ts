import { api } from '../../utils/api';
import moment from 'moment';
import { Summary } from '../../types';
import type { PageContextBuiltIn } from 'vite-plugin-ssr';

export { onBeforeRender };

async function onBeforeRender(pageContext: PageContextBuiltIn) {
    const summaries = await fetchBlogSummaries(pageContext);
    return {
        pageContext: {
            pageProps: {
                summaries: summaries,
            },
            documentProps: {title: 'Blog'},
        },
    };
}

async function fetchBlogSummaries(context: PageContextBuiltIn) {
    let response = await api.get('/blog/summaries', {params: context.urlParsed.search});
    return response.data.map((s: Summary) => {
        let postedDate = moment(s.posted);
        let formattedDate = postedDate.format('Do MMM YYYY');
        let timeAgo = postedDate.fromNow();
        s.posted = `${ formattedDate } (${ timeAgo })`;
        return s;
    });
}
