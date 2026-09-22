import { tool } from "@opencode-ai/plugin"

// Типизация ответа от Confluence API v2
interface ConfluencePage {
  id: string
  title: string
  status: string
  spaceId: string
  parentId?: string
  body?: {
    atlas_doc_format?: {
      value: string
      representation: string
    }
    storage?: {
      value: string
      representation: string
    }
  }
  version?: {
    createdAt: string
    message?: string
    number: number
  }
}

export default tool({
  description: "Получить страницу Confluence по pageId. Возвращает заголовок, содержимое и метаданные страницы.",

  args: {
    pageId: tool.schema.string({
      description: "ID страницы Confluence (числовой идентификатор из URL страницы)"
    }),
    format: tool.schema.string({
      description: "Формат содержимого: 'atlas_doc_format' (новый редактор) или 'storage' (HTML). По умолчанию: atlas_doc_format",
      default: "atlas_doc_format"
    }).optional()
  },

  async execute(args) {
    const baseUrl = process.env.CONFLUENCE_URL
    const email = process.env.CONFLUENCE_EMAIL
    const token = process.env.CONFLUENCE_API_TOKEN

    // Валидация переменных окружения
    if (!baseUrl || !email || !token) {
      throw new Error(
        "Не заданы переменные окружения Confluence. " +
        "Убедитесь, что установлены: CONFLUENCE_URL, CONFLUENCE_EMAIL, CONFLUENCE_API_TOKEN"
      )
    }

    // Валидация pageId
    if (!args.pageId || !/^\d+$/.test(args.pageId)) {
      throw new Error(`Некорректный pageId: "${args.pageId}". Ожидается числовой ID (например, 123456789)`)
    }

    const auth = Buffer.from(`${email}:${token}`).toString("base64")
    const format = args.format || "atlas_doc_format"

    // Добавляем таймаут для fetch (5 секунд)
    const controller = new AbortController()
    const timeoutId = setTimeout(() => controller.abort(), 5000)

    try {
      const response = await fetch(
        `${baseUrl}/wiki/api/v2/pages/${args.pageId}?body-format=${format}`,
        {
          method: "GET",
          headers: {
            Authorization: `Basic ${auth}`,
            Accept: "application/json"
          },
          signal: controller.signal
        }
      )

      // Детальная обработка ошибок по статусам
      if (response.status === 404) {
        throw new Error(`Страница с ID ${args.pageId} не найдена. Проверьте правильность ID и права доступа.`)
      }

      if (response.status === 403) {
        throw new Error(
          `Доступ запрещен (403). Убедитесь, что пользователь ${email} имеет право просмотра страницы.`
        )
      }

      if (response.status === 429) {
        throw new Error(
          "Превышен лимит запросов к Confluence API (429). Подождите и повторите попытку."
        )
      }

      if (!response.ok) {
        const errorText = await response.text().catch(() => "Неизвестная ошибка")
        throw new Error(
          `Confluence API error: ${response.status} ${response.statusText}\n${errorText}`
        )
      }

      const data: ConfluencePage = await response.json()

      // Возвращаем структурированный результат
      return JSON.stringify({
        success: true,
        pageId: data.id,
        title: data.title,
        status: data.status,
        spaceId: data.spaceId,
        version: data.version?.number,
        content: data.body?.atlas_doc_format?.value || data.body?.storage?.value || "Содержимое не найдено",
        contentFormat: format
      }, null, 2)

    } catch (error) {
      if (error instanceof Error && error.name === 'AbortError') {
        throw new Error("Превышено время ожидания ответа от Confluence API (5 секунд)")
      }
      throw error
    } finally {
      clearTimeout(timeoutId)
    }
  }
})