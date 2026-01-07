"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { Loader2 } from "lucide-react";

export default function AdminRootPage() {
    const router = useRouter();

    useEffect(() => {
        const session = localStorage.getItem("admin_session");
        if (session) {
            router.replace("/admin/import");
        } else {
            router.replace("/admin/login");
        }
    }, [router]);

    return (
        <div className="min-h-screen flex items-center justify-center bg-background">
            <Loader2 className="w-8 h-8 animate-spin text-primary" />
        </div>
    );
}
