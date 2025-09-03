/**
  Given two objects, returns a new object with only the fields that have changed.
 */
export function getChangedFields<T>(original: T, updated: T): Partial<T> {
    const changed: Partial<T> = {};

    for (const key in original) {
        if (updated[key] !== original[key])
            changed[key] = updated[key];
    }
    return changed;
}


export function camelToSnake(text: string): string {
    return text.replace(/[A-Z]/g, letter => `_${letter.toLowerCase()}`);
}

export function snakeToCamel(text: string): string {
    return text.replace(/(_\w)/g, letter => letter[1].toUpperCase());
}

/**
  Transforms the keys of an object from snake_case to camelCase.
 */
export function transformKeysToCamelCase<T extends Record<string, any>>(
  obj: T
): Record<string, any> {
  const result: Record<string, any> = {};

  for (const key in obj) {

    const camelKey = snakeToCamel(key);
    result[camelKey] = obj[key];
  }

  return result;
}

/**
  Transforms the keys of an object from camelCase to snake_case.
 */

export function transformKeysToSnakeCase<T extends Record<string, any>>(
  obj: T
): Record<string, any> {
  const result: Record<string, any> = {};

  for (const key in obj) {
    const snakeKey = camelToSnake(key);
    result[snakeKey] = obj[key];
  }

  return result;
}

/**
  Filters out any keys that have an undefined, null, or empty string value
 */
export function cleanedFilters(
  filters?: Record<string, any>
): Record<string, string> {
  if (!filters) return {};
  
  return Object.fromEntries(
    Object.entries(filters)
      .filter(([_, value]) => value !== undefined && value !== null && value !== "")
      .map(([key, value]) => [key, String(value)])
  );
}

export function formatDateString(date: string): string {
  const parsedDate = new Date(date);
  return parsedDate.toLocaleString("uk-UA", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  });
}