from skema.reconstruct import from_graphql
from graphql import build_schema


def test_1():
    print()
    s = """
    type X {
        a: String
        b: Int
    }
    interface Interface {
        a: String
    }
    interface Node {
        b: String
    }
    type Y implements Interface {
        a: String @direct
        b: X
    }
    union A = X | Y
    scalar Scalar

    directive @direct(
    reason: String = "No longer supported"
    ) on FIELD_DEFINITION | ENUM_VALUE

    type Listed {
        f: [X]
        j: String
    }

    input Input {
        a: Int
    }

    """
    skema = from_graphql(s)
    print(skema)

    skema = from_graphql(s2)
    print(skema)


s2 = """
scalar AnyScalar

type DataPoint {
  x: Float
  y: Float
  serviceName: String
}

scalar Date

scalar DateTime

enum Direction {
  ASC
  DESC
}

input GetLogsInput {
  serviceNames: [String]
  from: String
  to: String
  untilInsertId: String
}

type GetLogsNodes {
  nodes: [LogsNode]
  lastInsertId: String
}

scalar Json

type LogsNode {
  datetime: String
  line: String
  service: String
}

input MetricsInput {
  lastHours: Int
  binSecondsWidth: Int
  serviceNames: [String!]
  nowUnix: Int
}

scalar ObjectId

type PageInfo {
  startCursor: AnyScalar
  endCursor: AnyScalar
  hasNextPage: Boolean
  hasPreviousPage: Boolean
}

type Query {
  mongoke_version: String
  User(where: UserWhere): User
  Users(where: UserWhere, cursorField: UserFields, first: Int, last: Int, after: AnyScalar, before: AnyScalar): UserConnection!
  Stack(where: StackWhere): Stack
  Stacks(where: StackWhere, cursorField: StackFields, first: Int, last: Int, after: AnyScalar, before: AnyScalar): StackConnection!
  getLogs(input: GetLogsInput): GetLogsNodes
  getRequestsCountMetrics(input: MetricsInput): [DataPoint]
  getRequestsLatencyMetrics(input: MetricsInput): [DataPoint]
}

enum Region {
  asia_east1
  asia_northeast1
  europe_north1
  europe_west1
  europe_west4
  us_central1
  us_east1
  us_east4
  us_west1
}

type Service {
  name: String
  cloudConsoleName: String
  image: String
  url: String
  environmentJson: String
  isActive: Boolean
}

type Stack {
  name: String
  status: StackStatus
  region: Region
  _id: ObjectId
  createdAtUnix: Int
  deployedByUserUid: String
  terraformStateUrl: String
  dockerComposeJson: String
  dockerComposeYaml: String
  services: [Service]
  githubIntegration: StackGitIntegration
}

type StackConnection {
  nodes: [Stack]!
  edges: [StackEdge]!
  pageInfo: PageInfo!
}

type StackEdge {
  node: Stack
  cursor: AnyScalar
}

enum StackFields {
  name
  status
  region
  _id
  createdAtUnix
  deployedByUserUid
  terraformStateUrl
  dockerComposeJson
  dockerComposeYaml
}

type StackGitIntegration {
  url: String
}

enum StackStatus {
  CREATING
  ACTIVE
  ERROR
}

input StackWhere {
  and: [StackWhere]
  or: [StackWhere]
  name: WhereString
  status: WhereStackStatus
  region: WhereRegion
  _id: WhereObjectId
  createdAtUnix: WhereInt
  deployedByUserUid: WhereString
  terraformStateUrl: WhereString
  dockerComposeJson: WhereString
  dockerComposeYaml: WhereString
}

scalar Time

type User {
  uid: String
  stackIds: [String]
}

type UserConnection {
  nodes: [User]!
  edges: [UserEdge]!
  pageInfo: PageInfo!
}

type UserEdge {
  node: User
  cursor: AnyScalar
}

enum UserFields {
  uid
}

input UserWhere {
  and: [UserWhere]
  or: [UserWhere]
  uid: WhereString
}

input WhereBoolean {
  in: [Boolean]
  nin: [Boolean]
  eq: Boolean
  neq: Boolean
}

input WhereFloat {
  in: [Float]
  nin: [Float]
  eq: Float
  neq: Float
}

input WhereID {
  in: [ID]
  nin: [ID]
  eq: ID
  neq: ID
}

input WhereInt {
  in: [Int]
  nin: [Int]
  eq: Int
  neq: Int
}

input WhereObjectId {
  in: [ObjectId]
  nin: [ObjectId]
  eq: ObjectId
  neq: ObjectId
}

input WhereRegion {
  in: [Region]
  nin: [Region]
  eq: Region
  neq: Region
}

input WhereStackStatus {
  in: [StackStatus]
  nin: [StackStatus]
  eq: StackStatus
  neq: StackStatus
}

input WhereString {
  in: [String]
  nin: [String]
  eq: String
  neq: String
}
"""

