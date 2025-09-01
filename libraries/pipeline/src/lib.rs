//! Dora 配置文件解析库
//! 
//! 支持 YAML、JSON、TOML 格式的读写

pub mod config;
pub mod format;

pub use config::{Config, Domains, Node};
pub use format::{ConfigFormat, read_config, write_config};