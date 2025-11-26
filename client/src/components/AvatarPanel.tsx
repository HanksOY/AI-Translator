import { motion } from "framer-motion";
import avatarImage from "@assets/cPort-avatar image_1763858388946.png";

interface AvatarPanelProps {
  isActive?: boolean;
}

export default function AvatarPanel({ isActive = false }: AvatarPanelProps) {
  return (
    <div className="relative h-full flex flex-col bg-card border-r">
      <div className="absolute inset-0 bg-gradient-to-br from-primary/5 via-transparent to-primary/10" />
      
      <div className="flex-1 flex items-center justify-center p-6">
        <motion.div
          className="relative w-full max-w-md rounded-md overflow-hidden border-2 border-primary/20"
          animate={isActive ? { scale: [1, 1.02, 1] } : {}}
          transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
        >
          <img
            src={avatarImage}
            alt="AI Avatar"
            className="w-full h-full object-cover"
            data-testid="img-avatar"
          />
          
          {isActive && (
            <motion.div
              className="absolute inset-0 border-2 border-primary/50 rounded-md"
              animate={{ opacity: [0.3, 0.7, 0.3] }}
              transition={{ duration: 1.5, repeat: Infinity, ease: "easeInOut" }}
            />
          )}
          
          <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-background/90 to-transparent p-4">
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              {isActive ? (
                <>
                  <motion.div
                    className="w-2 h-2 rounded-full bg-primary"
                    animate={{ scale: [1, 1.3, 1] }}
                    transition={{ duration: 1, repeat: Infinity }}
                    data-testid="status-active"
                  />
                  <span>AI Avatar Active</span>
                </>
              ) : (
                <>
                  <div className="w-2 h-2 rounded-full bg-muted-foreground/50" data-testid="status-inactive" />
                  <span>AI Avatar Standby</span>
                </>
              )}
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
