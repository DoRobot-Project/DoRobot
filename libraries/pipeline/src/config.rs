//! 配置结构体定义

use serde::{Deserialize, Serialize};
use std::collections::HashMap;

/// 主配置结构体
#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct Config {
    pub domains: Domains,
}

/// Domains 部分
#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct Domains {
    pub nodes: Vec<Node>,
}

/// 节点配置
#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct Node {
    pub id: String,
    pub path: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub inputs: Option<HashMap<String, String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub outputs: Option<Vec<String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub env: Option<HashMap<String, String>>,
}

impl Config {
    /// 创建新的空配置
    pub fn new() -> Self {
        Config {
            domains: Domains {
                nodes: Vec::new(),
            },
        }
    }

    /// 获取所有节点
    pub fn nodes(&self) -> &[Node] {
        &self.domains.nodes
    }

    /// 根据 ID 查找节点
    pub fn find_node(&self, id: &str) -> Option<&Node> {
        self.domains.nodes.iter().find(|node| node.id == id)
    }

    /// 添加节点
    pub fn add_node(&mut self, node: Node) {
        self.domains.nodes.push(node);
    }
}

impl Default for Config {
        fn default() -> Self {
        Self::new()
    }
}