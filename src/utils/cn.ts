type ClassValue = string | number | null | undefined | false;

/** Joins truthy class names together. A tiny dependency-free `clsx`. */
export function cn(...values: ClassValue[]): string {
  return values.filter(Boolean).join(" ");
}
