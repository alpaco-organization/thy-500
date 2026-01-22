import { useState } from "react";
import { useNotification } from "@/contexts/notification-context";
import { useLanguage } from "@/contexts/language-context";

interface IOptions<T = any> {
  params?: Record<string, any>;
  onSuccess?: (data: T) => void;
  onError?: (error: string) => void;
  onLoading?: (loading: boolean) => void;
}

const useFetch = (method: "GET" | "POST", path: string) => {
  const { showNotification } = useNotification();
  const { currentLanguage } = useLanguage();
  
  const [data, setData] = useState<any | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

const API_BASE_URL =
  process.env.INTERNAL_API_BASE_URL ?? "http://localhost:8000/api/";

  const doFetch = async (options: IOptions = {}) => {
    if (loading) return;

    const { params, onSuccess, onError, onLoading } = options;

    setLoading(true);
    setError(null);
    setData(null);
    onLoading?.(true);

    try {
      let parameters = "";

      if (method === "GET" && params && Object.keys(params).length > 0) {
        const parsedParams = JSON.parse(JSON.stringify(params));
        parameters = "?" + new URLSearchParams(parsedParams).toString();
      }

      const response = await fetch(
        `${API_BASE_URL}${path}${method === "GET" ? parameters : ""}`,
        {
          method,
          headers: {
            "Accept-Language": currentLanguage,
            ...(method === "POST" && { "Content-Type": "application/json" }),
          },
          ...(method === "POST" && { body: JSON.stringify(params) }),
        },
      );

      const result = await response.json();

      if(!response.ok){
        throw new Error((result.detail));
      }

      setData(result);
      await onSuccess?.(result);
    } catch (error) {
      if (error instanceof Error) {
        setError(error.message);
        showNotification(error.message);
        await onError?.(error.message);
      }
    } finally {
      setLoading(false);
      onLoading?.(false);
    }
  };

  return { data, error, loading, fetch: doFetch };
};

export default useFetch;