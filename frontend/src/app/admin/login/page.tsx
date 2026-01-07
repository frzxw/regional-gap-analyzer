"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Lock } from "lucide-react";

export default function AdminLoginPage() {
    const [loading, setLoading] = useState(false);
    const router = useRouter();

    useEffect(() => {
        const session = localStorage.getItem("admin_session");
        if (session) {
            router.replace("/admin/import");
        }
    }, [router]);

    const handleLogin = (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);

        // Fake login simulation
        setTimeout(() => {
            // Set session marker
            localStorage.setItem("admin_session", "true");

            // Redirect to admin panel
            router.push("/admin/import");
        }, 800);
    };

    return (
        <div className="min-h-screen grid place-items-center bg-gradient-to-br from-background to-muted">
            <Card className="w-full max-w-md shadow-2xl bg-card/80 backdrop-blur-sm">
                <CardHeader className="text-center space-y-4">
                    <div className="mx-auto w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center">
                        <Lock className="w-6 h-6 text-primary" />
                    </div>
                    <div className="space-y-2">
                        <CardTitle className="text-2xl">Admin Access</CardTitle>
                        <CardDescription>
                            Silakan masuk untuk mengelola data
                        </CardDescription>
                    </div>
                </CardHeader>
                <CardContent>
                    <form onSubmit={handleLogin} className="space-y-4">
                        <div className="space-y-2">
                            <Input
                                type="text"
                                placeholder="Username"
                                required
                                className="bg-background/50"
                            />
                        </div>
                        <div className="space-y-2">
                            <Input
                                type="password"
                                placeholder="Password"
                                required
                                className="bg-background/50"
                            />
                        </div>
                        <Button className="w-full" size="lg" disabled={loading}>
                            {loading ? "Verifying..." : "Masuk Dashboard"}
                        </Button>
                    </form>
                </CardContent>
            </Card>
        </div>
    );
}
