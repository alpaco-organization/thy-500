export interface IPerson {
  personId: string;
  name: string;
  x: number;
  y: number;
  z: number;
}

export type SearchType = "identity" | "fullName";