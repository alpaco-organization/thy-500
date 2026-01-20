"use client";

import { clsx } from "clsx";
import { CircleAlert, CircleCheck } from "lucide-react";
import { createContext, useContext, useState } from "react";

type NotificationType = "error" | "success";

interface INotification {
  message: string;
  type: NotificationType;
}

interface NotificationContextTypes {
  notifications: INotification[];
  showNotification: (message: string, type?: NotificationType) => void;
}

const NotificationContextDefaultValues: NotificationContextTypes = {
  notifications: [],
  showNotification: () => {},
};

const NotificationContext = createContext<NotificationContextTypes>(
  NotificationContextDefaultValues,
);

export function NotificationProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const [notifications, setNotifications] = useState<INotification[]>([]);

  const calculateTimeout = (message: string) => {
    return Math.max(message.length * 50, 5000);
  };

  const showNotification = (message: string, type?: NotificationType) => {
    const newNotification = {
      message: message,
      type: type || "error",
    };
    setNotifications((prev) => [...prev, newNotification]);

    setTimeout(() => {
      setNotifications((prev) => prev.slice(1));
    }, calculateTimeout(message));
  };

  const value = {
    notifications,
    showNotification,
  };

  return (
    <NotificationContext.Provider value={value}>
      <Notifications />
      {children}
    </NotificationContext.Provider>
  );
}

export function useNotification() {
  return useContext(NotificationContext);
}

function Notifications() {
  const { notifications } = useNotification();

  return (
    <div className="fixed top-1/6 left-1/2 transform -translate-x-1/2 z-200 flex flex-col space-y-3">
      {notifications.map((notification: INotification, index: number) => (
        <Notification key={index} notification={notification} />
      ))}
    </div>
  );
}

function Notification({ notification }: { notification: INotification }) {
  const notificationIcons = {
    error: <CircleAlert className="size-4 shrink-0" />,
    success: <CircleCheck className="size-4 shrink-0" />,
  }

  return (
    <div className={clsx("border-2 rounded-2xl backdrop-blur-lg text-white px-4 py-2 animate-in fade-in text-sm slide-in-from-top-2 duration-300 text-center flex items-center gap-2", {
      "bg-primary/50 border-primary": notification.type === "error",
      "border-[#41424F]/80 bg-[#010101]/40": notification.type === "success",
    })}>
      {notificationIcons[notification.type]}
      {notification.message}
    </div>
  );
}
