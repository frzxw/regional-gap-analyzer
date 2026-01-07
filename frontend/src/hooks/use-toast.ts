"use client";

import { useState } from "react";

type ToastProps = {
    title?: string;
    description?: string;
    action?: React.ReactNode;
    variant?: "default" | "destructive";
};

let listeners: ((toasts: ToastProps[]) => void)[] = [];
let toasts: ToastProps[] = [];

function notifyListeners() {
    listeners.forEach((listener) => listener([...toasts]));
}

export function useToast() {
    const [state, setState] = useState<ToastProps[]>(toasts);

    function toast(props: ToastProps) {
        toasts = [...toasts, props];
        notifyListeners();

        // Auto dismiss after 3 seconds
        setTimeout(() => {
            toasts = toasts.filter((t) => t !== props);
            notifyListeners();
        }, 3000);
    }

    // Subscribe to changes
    if (!listeners.includes(setState)) {
        listeners.push(setState);
    }

    return {
        toast,
        toasts: state,
        dismiss: (id: string) => { },
    };
}
