// This file is auto-generated by @hey-api/openapi-ts

export const ChapterSchema = {
    properties: {
        content: {
            type: 'string',
            title: 'Content',
            description: 'El contenido detallado del capítulo'
        },
        image_description: {
            type: 'string',
            title: 'Image Description',
            description: `
Descripción detallada para la generación de una imagen clave del capítulo, 
la descripción debe ser en inglés y debe ser lo más detallada posible
        `
        },
        id: {
            type: 'integer',
            title: 'Id',
            description: 'El ID del capítulo'
        },
        title: {
            type: 'string',
            title: 'Title',
            description: 'El título del capítulo'
        },
        image_url: {
            anyOf: [
                {
                    type: 'string'
                },
                {
                    type: 'null'
                }
            ],
            title: 'Image Url',
            description: 'La URL de la imagen del capítulo'
        }
    },
    type: 'object',
    required: ['content', 'image_description', 'id', 'title', 'image_url'],
    title: 'Chapter'
} as const;

export const HTTPValidationErrorSchema = {
    properties: {
        detail: {
            items: {
                '$ref': '#/components/schemas/ValidationError'
            },
            type: 'array',
            title: 'Detail'
        }
    },
    type: 'object',
    title: 'HTTPValidationError'
} as const;

export const HealthCheckResponseSchema = {
    properties: {
        status: {
            type: 'string',
            title: 'Status'
        }
    },
    type: 'object',
    required: ['status'],
    title: 'HealthCheckResponse'
} as const;

export const StorySchema = {
    properties: {
        id: {
            anyOf: [
                {
                    type: 'string'
                },
                {
                    type: 'null'
                }
            ],
            title: 'Id'
        },
        created_at: {
            type: 'string',
            format: 'date-time',
            title: 'Created At'
        },
        updated_at: {
            type: 'string',
            format: 'date-time',
            title: 'Updated At'
        },
        title: {
            type: 'string',
            title: 'Title'
        },
        image_url: {
            type: 'string',
            title: 'Image Url'
        },
        premise: {
            type: 'string',
            title: 'Premise'
        },
        chapters: {
            items: {
                '$ref': '#/components/schemas/Chapter'
            },
            type: 'array',
            title: 'Chapters'
        },
        preferences: {
            '$ref': '#/components/schemas/UserPreferences'
        }
    },
    type: 'object',
    required: ['title', 'image_url', 'premise', 'chapters', 'preferences'],
    title: 'Story'
} as const;

export const UserPreferencesSchema = {
    properties: {
        genre: {
            type: 'string',
            title: 'Genre',
            description: 'El género literario de la historia'
        },
        length: {
            type: 'string',
            title: 'Length',
            description: 'La longitud deseada de la historia (corta, media, larga)'
        },
        style: {
            type: 'string',
            title: 'Style',
            description: 'El estilo de escritura deseado'
        },
        themes_to_include: {
            items: {
                type: 'string'
            },
            type: 'array',
            title: 'Themes To Include',
            description: 'Lista de temas que deben incluirse en la historia'
        },
        themes_to_avoid: {
            items: {
                type: 'string'
            },
            type: 'array',
            title: 'Themes To Avoid',
            description: 'Lista de temas que deben evitarse en la historia'
        },
        art_style: {
            type: 'string',
            title: 'Art Style',
            description: 'El estilo artístico deseado para las imágenes'
        }
    },
    type: 'object',
    required: ['genre', 'length', 'style', 'themes_to_include', 'themes_to_avoid', 'art_style'],
    title: 'UserPreferences'
} as const;

export const ValidationErrorSchema = {
    properties: {
        loc: {
            items: {
                anyOf: [
                    {
                        type: 'string'
                    },
                    {
                        type: 'integer'
                    }
                ]
            },
            type: 'array',
            title: 'Location'
        },
        msg: {
            type: 'string',
            title: 'Message'
        },
        type: {
            type: 'string',
            title: 'Error Type'
        }
    },
    type: 'object',
    required: ['loc', 'msg', 'type'],
    title: 'ValidationError'
} as const;