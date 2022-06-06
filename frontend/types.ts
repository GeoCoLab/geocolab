export type StringDict = {
    [index: string]: string
}

export type Tag = {
    id: number,
    name: string
}

export type Summary = {
    id: number,
    slug: string,
    title: string,
    posted: string,
    summary: string,
    tags: Array<Tag>,
    author: {
        id: number,
        name: string
    }
}

export type Component = any

export type PageContext = {
    Page: Component
    pageProps: Record<string, unknown>
    pageExports: {
        documentProps?: {
            title: string
        }
    }
    documentProps?: {
        title: string
    }
}

export type User = {
        country: string | null
        created: string | null
        email: string | null
        id: number | null
        name: string | null
        role: string | null
        todo: Array<string>,
        gravatar: string | null
        completion: number,
        given_name: string | null,
        family_name: string | null,
        given_name_first: boolean
    }
