"use client";

import { CircleAlert } from "lucide-react";
import { createContext, useContext, useState } from "react";

interface NotificationTypes {
  message: string;
}

interface NotificationContextTypes {
  notifications: NotificationTypes[];
  showNotification: (message: string) => void;
  clearAllNotifications: () => void;
}

const NotificationContextDefaultValues: NotificationContextTypes = {
  notifications: [],
  showNotification: () => {},
  clearAllNotifications: () => {},
};

const NotificationContext = createContext<NotificationContextTypes>(
  NotificationContextDefaultValues,
);

export function NotificationProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const [notifications, setNotifications] = useState<NotificationTypes[]>([]);

  const calculateTimeout = (message: string) => {
    return Math.max(message.length * 50, 5000);
  };

  const showNotification = (message: string) => {
    const newNotification = {
      message: message,
    };
    setNotifications((prev) => [...prev, newNotification]);

    setTimeout(() => {
      setNotifications((prev) => prev.slice(1));
    }, calculateTimeout(message));
  };

  const removeNotification = (index: number) => {
    setNotifications((prev) => prev.filter((_, i) => i !== index));
  };

  const clearAllNotifications = () => {
    setNotifications([]);
  };

  const value = {
    notifications,
    showNotification,
    clearAllNotifications,
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
      {notifications.map((notification: NotificationTypes, index: number) => (
        <Notification key={index} notification={notification} />
      ))}
    </div>
  );
}

function Notification({ notification }: { notification: NotificationTypes }) {
  return (
    <div className="bg-primary/50 border-2 rounded-full border-primary backdrop-blur-lg text-white px-4 py-2 animate-in fade-in text-sm slide-in-from-top-2 duration-300 text-center flex items-center gap-2">
      <CircleAlert className="size-4" />
      {notification.message}
    </div>
  );
}
