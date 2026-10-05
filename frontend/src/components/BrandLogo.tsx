import React from 'react';

interface BrandLogoProps {
  size?: 'sm' | 'md' | 'lg';
  showTagline?: boolean;
}

export const BrandLogo: React.FC<BrandLogoProps> = ({
  size = 'md',
  showTagline = true,
}) => {
  const sealDimensions = size === 'sm' ? 44 : size === 'lg' ? 68 : 52;

  return (
    <div className={`sweet-brand-logo-wrap size-${size}`}>
      {/* ── Dangling & Shining Circular Seal Emblem ── */}
      <div className="logo-charm-anchor">
        <div className="logo-hanging-charm">
          {/* Top Hanging Ring / Eyelet */}
          <div className="charm-eyelet" />

          {/* Circular Rose-Gold Seal */}
          <div className="charm-seal-disc">
            <svg
              className="seal-svg"
              viewBox="0 0 120 120"
              width={sealDimensions}
              height={sealDimensions}
              xmlns="http://www.w3.org/2000/svg"
            >
              <defs>
                {/* Rose Gold Metallic Outer Gradient */}
                <linearGradient id="roseGoldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#E5B299" />
                  <stop offset="25%" stopColor="#F8D7C9" />
                  <stop offset="50%" stopColor="#E8A0BF" />
                  <stop offset="75%" stopColor="#F5D5E0" />
                  <stop offset="100%" stopColor="#C98A7D" />
                </linearGradient>

                {/* Inner Disc Gradient */}
                <linearGradient id="discBg" x1="0%" y1="0%" x2="0%" y2="100%">
                  <stop offset="0%" stopColor="#FFFDFB" />
                  <stop offset="100%" stopColor="#FFF2F6" />
                </linearGradient>

                {/* Heart Wax Seal Gradient */}
                <linearGradient id="heartSealGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#FF7597" />
                  <stop offset="50%" stopColor="#E85B86" />
                  <stop offset="100%" stopColor="#C83B65" />
                </linearGradient>

                {/* Vintage Key Rose-Gold Gradient */}
                <linearGradient id="keyGoldGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" stopColor="#C98A7D" />
                  <stop offset="50%" stopColor="#E5B299" />
                  <stop offset="100%" stopColor="#B37365" />
                </linearGradient>

                {/* Curved Path for Top Text */}
                <path
                  id="topArchPath"
                  d="M 18,60 A 42,42 0 0,1 102,60"
                  fill="none"
                />

                {/* Curved Path for Bottom Text */}
                <path
                  id="bottomArchPath"
                  d="M 104,60 A 44,44 0 0,1 16,60"
                  fill="none"
                />
              </defs>

              {/* Outer Metallic Ring */}
              <circle
                cx="60"
                cy="60"
                r="56"
                fill="url(#roseGoldGrad)"
                stroke="#D48B9A"
                strokeWidth="1"
              />

              {/* Inner Base Disc */}
              <circle
                cx="60"
                cy="60"
                r="52"
                fill="url(#discBg)"
              />

              {/* Dotted Accent Ring */}
              <circle
                cx="60"
                cy="60"
                r="49"
                fill="none"
                stroke="#E8A0BF"
                strokeWidth="1.2"
                strokeDasharray="2, 2.5"
                opacity="0.85"
              />

              {/* Inner Thin Border */}
              <circle
                cx="60"
                cy="60"
                r="37"
                fill="none"
                stroke="#E5B299"
                strokeWidth="1"
                opacity="0.6"
              />

              {/* ── Top Curved Text: Sweet Sentiments ── */}
              <text
                className="seal-curved-text-top"
                fontSize="11.5"
                fontFamily="'Playfair Display', 'Cormorant Garamond', Georgia, serif"
                fontWeight="700"
                fill="#4A3439"
                letterSpacing="0.4"
              >
                <textPath href="#topArchPath" startOffset="50%" textAnchor="middle">
                  Sweet Sentiments
                </textPath>
              </text>

              {/* ── Bottom Curved Text: Curated Gifts & Sweet Treats ── */}
              <text
                className="seal-curved-text-bottom"
                fontSize="5.2"
                fontFamily="'DM Sans', sans-serif"
                fontWeight="700"
                fill="#A67B88"
                letterSpacing="1.2"
              >
                <textPath href="#bottomArchPath" startOffset="50%" textAnchor="middle">
                  • CURATED GIFTS & SWEET TREATS •
                </textPath>
              </text>

              {/* ── Center Envelope ── */}
              <g className="seal-envelope-group" transform="translate(0, -1)">
                {/* Envelope Back / Base */}
                <rect
                  x="42"
                  y="47"
                  width="36"
                  height="23"
                  rx="2.5"
                  fill="#FFFBF7"
                  stroke="#C98A7D"
                  strokeWidth="1.2"
                />

                {/* Envelope Bottom Folds */}
                <path
                  d="M 42 70 L 60 58 L 78 70"
                  fill="#FFF5F7"
                  stroke="#E5B299"
                  strokeWidth="1"
                />
                <path
                  d="M 42 47 L 60 61 L 78 47"
                  fill="#FFF0F5"
                  stroke="#C98A7D"
                  strokeWidth="1.2"
                />

                {/* Heart Wax Seal on Envelope */}
                <g transform="translate(60, 58) scale(0.9)">
                  <path
                    d="M 0 3 C -5 -3, -10 1, -10 6 C -10 11, 0 17, 0 17 C 0 17, 10 11, 10 6 C 10 1, 5 -3, 0 3 Z"
                    fill="url(#heartSealGrad)"
                    transform="translate(0, -9)"
                    filter="drop-shadow(0 1px 2px rgba(200, 59, 101, 0.35))"
                  />
                  {/* Wax Seal Highlight */}
                  <ellipse cx="-3" cy="-5" rx="1.5" ry="0.8" fill="#FFAEC3" opacity="0.8" />
                </g>
              </g>

              {/* ── Center Vintage Heart Key ── */}
              <g className="seal-key-group" transform="translate(60, 77) rotate(-10) scale(0.95)">
                {/* Heart Shaped Key Bow */}
                <path
                  d="M -15 0 C -18 -4, -22 -1, -22 3 C -22 7, -15 12, -15 12 C -15 12, -8 7, -8 3 C -8 -1, -12 -4, -15 0 Z"
                  fill="none"
                  stroke="url(#keyGoldGrad)"
                  strokeWidth="1.5"
                  transform="translate(0, -5)"
                />
                {/* Key Stem */}
                <line
                  x1="-7"
                  y1="0"
                  x2="15"
                  y2="0"
                  stroke="url(#keyGoldGrad)"
                  strokeWidth="1.8"
                  strokeLinecap="round"
                />
                {/* Key Bit Teeth */}
                <line x1="10" y1="0" x2="10" y2="4.5" stroke="url(#keyGoldGrad)" strokeWidth="1.5" strokeLinecap="round" />
                <line x1="13.5" y1="0" x2="13.5" y2="3.5" stroke="url(#keyGoldGrad)" strokeWidth="1.5" strokeLinecap="round" />
              </g>

              {/* ── Decorative Gold Sparkles ── */}
              <path
                d="M 33 52 L 34 54.5 L 36.5 55.5 L 34 56.5 L 33 59 L 32 56.5 L 29.5 55.5 L 32 54.5 Z"
                fill="#F59E0B"
                opacity="0.9"
              />
              <path
                d="M 87 52 L 88 54.5 L 90.5 55.5 L 88 56.5 L 87 59 L 86 56.5 L 83.5 55.5 L 86 54.5 Z"
                fill="#F59E0B"
                opacity="0.9"
              />
            </svg>

            {/* Glowing Light Beam Shimmer Layer */}
            <div className="seal-shine-sweep" />
          </div>
        </div>
      </div>

      {/* ── Artistic Calligraphy Typography ── */}
      <div className="brand-calligraphy-block">
        <div className="calligraphy-title-row">
          <span className="calligraphy-word">Sweet Sentiments</span>
          <span className="calligraphy-flourish-heart">♡</span>
        </div>
        {showTagline && (
          <div className="calligraphy-tagline">
            <span className="tagline-star">✧</span>
            <span>CURATED GIFTS & SWEET TREATS</span>
            <span className="tagline-star">✧</span>
          </div>
        )}
      </div>
    </div>
  );
};
