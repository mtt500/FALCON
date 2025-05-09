import React from "react";
import ReactMarkdown from "react-markdown"; // 用于渲染Markdown
import styles from "@/app/report/markdown.module.css"

const MarkdownRenderer = ({ content }: { content: string }) => {
  return (
    <div className={styles.prose}>
      <ReactMarkdown>
        {content}
      </ReactMarkdown>
    </div>
  );
};

export default MarkdownRenderer;
