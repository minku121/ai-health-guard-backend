import { Navbar, Button, Link } from "@nextui-org/react";

interface LayoutProps {
  children: React.ReactNode;
}

export default function Layout({ children }: LayoutProps) {
  return (
    <div className="min-h-screen bg-background">
      <Navbar className="bg-background/60 backdrop-blur-md border-b border-divider">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between h-16">
            <Link href="/" className="text-xl font-bold text-primary">
              AI Health Guard
            </Link>
            <div className="flex gap-4">
              <Button as={Link} href="/" color="primary" variant="ghost">
                Symptoms
              </Button>
              <Button as={Link} href="/pregnancy" color="primary" variant="ghost">
                Pregnancy
              </Button>
              <Button as={Link} href="/heart" color="primary" variant="ghost">
                Heart
              </Button>
              <Button as={Link} href="/diabetes" color="primary" variant="ghost">
                Diabetes
              </Button>
            </div>
          </div>
        </div>
      </Navbar>
      <main>{children}</main>
    </div>
  );
} 