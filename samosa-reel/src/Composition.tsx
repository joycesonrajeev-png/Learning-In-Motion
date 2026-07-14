import { CalculateMetadataFunction, Composition, Sequence, AbsoluteFill, useCurrentFrame, interpolate } from "remotion";
import { useState, useEffect } from "react";

type Props = {};

const calculateMetadata: CalculateMetadataFunction<Props> = () => {
  return {};
};

export const MyComposition = () => {
  return (
    <Composition
      id="SamoaReel"
      component={SamoaReelComponent}
      durationInFrames={450}
      fps={30}
      width={1080}
      height={1920}
      calculateMetadata={calculateMetadata}
    />
  );
};

const AnimatedText: React.FC<{ text: string; startFrame: number; endFrame: number; fontSize?: number; delay?: number }> = ({
  text,
  startFrame,
  endFrame,
  fontSize = 72,
  delay = 0,
}) => {
  const frame = useCurrentFrame();
  const isVisible = frame >= startFrame;

  const opacity = interpolate(
    frame,
    [startFrame + delay, startFrame + delay + 15],
    [0, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  const scale = interpolate(
    frame,
    [startFrame + delay, startFrame + delay + 15],
    [0.8, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  if (!isVisible) return null;

  return (
    <div
      style={{
        opacity,
        transform: `scale(${scale})`,
        fontSize: fontSize,
        fontWeight: "bold",
        color: "#ffffff",
        textAlign: "center",
        transition: "all 0.3s ease",
      }}
    >
      {text}
    </div>
  );
};

const SwipeUpAnimation: React.FC<{ startFrame: number; endFrame: number }> = ({ startFrame, endFrame }) => {
  const frame = useCurrentFrame();

  const yTranslate = interpolate(
    frame,
    [startFrame, endFrame],
    [100, -1920],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  const opacity = interpolate(
    frame,
    [startFrame, startFrame + 10, endFrame - 10, endFrame],
    [0, 1, 1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  return (
    <div
      style={{
        position: "absolute",
        bottom: 0,
        left: 0,
        right: 0,
        height: "300px",
        background: "linear-gradient(to top, rgba(0, 150, 255, 0.8), transparent)",
        transform: `translateY(${yTranslate}px)`,
        opacity,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        fontSize: 48,
        fontWeight: "bold",
        color: "#ffffff",
      }}
    >
      ↑ Swipe Up
    </div>
  );
};

export const SamoaReelComponent: React.FC<Props> = () => {
  return (
    <AbsoluteFill
      style={{
        background: "#0a0a0a",
        overflow: "hidden",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        padding: 40,
        gap: 40,
      }}
    >
      {/* Background accent circles */}
      <div
        style={{
          position: "absolute",
          width: "400px",
          height: "400px",
          background: "radial-gradient(circle, rgba(0, 150, 255, 0.1), transparent)",
          borderRadius: "50%",
          top: "-100px",
          right: "-100px",
        }}
      />
      <div
        style={{
          position: "absolute",
          width: "300px",
          height: "300px",
          background: "radial-gradient(circle, rgba(255, 255, 255, 0.05), transparent)",
          borderRadius: "50%",
          bottom: "-50px",
          left: "-50px",
        }}
      />

      {/* Title */}
      <Sequence from={0} durationInFrames={90}>
        <div
          style={{
            fontSize: 64,
            fontWeight: "bold",
            color: "#0096ff",
            textAlign: "center",
            lineHeight: 1.2,
          }}
        >
          Are you craving
          <br />
          Indian Food?
        </div>
      </Sequence>

      {/* Bullet points container */}
      <Sequence from={90} durationInFrames={240}>
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            gap: 30,
            width: "100%",
            paddingLeft: 40,
            paddingRight: 40,
          }}
        >
          <BulletPoint text="1. Low In Carbs" frameIndex={0} />
          <BulletPoint text="2. Low Blood Sugar" frameIndex={60} />
          <BulletPoint text="3. Want Something Spicy" frameIndex={120} />
        </div>
      </Sequence>

      {/* Call to action */}
      <Sequence from={330} durationInFrames={120}>
        <div
          style={{
            fontSize: 56,
            fontWeight: "bold",
            color: "#ffffff",
            textAlign: "center",
            lineHeight: 1.3,
            textShadow: "0 4px 8px rgba(0, 150, 255, 0.4)",
          }}
        >
          Call the
          <br />
          <span style={{ color: "#0096ff" }}>Samosa Samurai</span>
        </div>
      </Sequence>

      {/* Swipe up animation */}
      <SwipeUpAnimation startFrame={330} endFrame={450} />
    </AbsoluteFill>
  );
};

const BulletPoint: React.FC<{ text: string; frameIndex: number }> = ({ text, frameIndex }) => {
  const frame = useCurrentFrame() - 90;

  const isVisible = frame >= frameIndex;
  const opacity = interpolate(
    frame,
    [frameIndex, frameIndex + 20],
    [0, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  const scale = interpolate(
    frame,
    [frameIndex, frameIndex + 20],
    [0.7, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  const translateX = interpolate(
    frame,
    [frameIndex, frameIndex + 20],
    [-50, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  if (!isVisible) return null;

  return (
    <div
      style={{
        fontSize: 48,
        fontWeight: "bold",
        color: "#ffffff",
        opacity,
        transform: `scale(${scale}) translateX(${translateX}px)`,
        display: "flex",
        alignItems: "center",
        gap: 20,
      }}
    >
      <span style={{ color: "#0096ff", fontSize: 56 }}>●</span>
      {text}
    </div>
  );
};
